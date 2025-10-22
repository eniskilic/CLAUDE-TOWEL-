"""
Amazon Towel Order Parser - Streamlit Application
Parses Amazon packing slip PDFs, generates labels, and creates production summaries
"""

import streamlit as st
import pdfplumber
import pandas as pd
import re
from io import BytesIO
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Amazon Towel Order Parser",
    page_icon="🧺",
    layout="wide"
)

# Initialize session state
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None


class OrderParser:
    """Parses Amazon packing slip PDFs for towel orders"""
    
    # Product type mapping from SKU prefix
    PRODUCT_TYPES = {
        'Set-6Pcs': '6-Piece Towel Set',
        'Set-3Pcs': '3-Piece Towel Set',
        'HT-2Pcs': '2-Piece Hand Towel',
        'BT-2Pcs': '2-Piece Bath Towel',
        'BS-1Pcs': 'Bath Sheet'
    }
    
    # Production equivalents for 3-piece sets
    PRODUCTION_MULTIPLIERS = {
        'Set-6Pcs': 2.0,
        'Set-3Pcs': 1.0,
        'HT-2Pcs': 0.0,  # Counted separately
        'BT-2Pcs': 0.0,  # Counted separately
        'BS-1Pcs': 0.0   # Listed separately
    }
    
    # Thread color Spanish translations
    THREAD_COLORS_ES = {
        'White': 'Blanco',
        'Black': 'Negro',
        'Navy': 'Azul Marino',
        'Gray': 'Gris',
        'Brown': 'Marrón',
        'Red': 'Rojo',
        'Pink': 'Rosa',
        'Blue': 'Azul',
        'Green': 'Verde',
        'Yellow': 'Amarillo',
        'Orange': 'Naranja',
        'Purple': 'Púrpura',
        'Beige': 'Beige',
        'Cream': 'Crema',
        'Ivory': 'Marfil'
    }
    
    def __init__(self):
        self.orders = []
        
    def parse_pdf(self, pdf_file, filename):
        """Parse a single PDF file"""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                pages_text = [page.extract_text() for page in pdf.pages]
                return self._process_pages(pages_text, filename)
        except Exception as e:
            st.error(f"Error parsing {filename}: {str(e)}")
            return []
    
    def _process_pages(self, pages_text, filename):
        """Process all pages and group into orders"""
        orders = []
        current_order = None
        
        for page_idx, text in enumerate(pages_text):
            if not text:
                continue
                
            # Check if this page starts a new order
            order_id_match = re.search(r'Order ID:\s*([0-9-]+)', text)
            
            if order_id_match:
                # New order detected
                if current_order:
                    orders.extend(self._extract_items_from_order(current_order, filename))
                
                current_order = {
                    'order_id': order_id_match.group(1),
                    'text': text,
                    'page': page_idx + 1
                }
            elif current_order:
                # Continuation page - merge with current order
                # Verify buyer name/address match (90% similarity would be implemented here)
                current_order['text'] += '\n' + text
            else:
                # First page without Order ID - try to extract buyer info
                buyer_match = re.search(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', text, re.MULTILINE)
                if buyer_match:
                    current_order = {
                        'order_id': f'UNKNOWN-{page_idx+1}',
                        'text': text,
                        'page': page_idx + 1
                    }
        
        # Process last order
        if current_order:
            orders.extend(self._extract_items_from_order(current_order, filename))
        
        return orders
    
    def _extract_items_from_order(self, order_data, filename):
        """Extract individual items from an order"""
        text = order_data['text']
        order_id = order_data['order_id']
        
        # Extract buyer name
        buyer_name = self._extract_buyer_name(text)
        
        # Extract gift message
        gift_message = self._extract_gift_message(text)
        
        # Find all SKU blocks
        items = []
        
        # Pattern to find SKU lines and their customization blocks
        sku_pattern = r'(Set-\d+Pcs|HT-\d+Pcs|BT-\d+Pcs|BS-\d+Pcs)-([A-Za-z]+)'
        matches = list(re.finditer(sku_pattern, text))
        
        for match in matches:
            sku = match.group(0)
            sku_pos = match.start()
            
            # Get text block after SKU (next 500 chars for customization details)
            block_end = min(sku_pos + 500, len(text))
            block = text[sku_pos:block_end]
            
            # Extract details from this block
            item = {
                'order_id': order_id,
                'buyer_name': buyer_name,
                'sku': sku,
                'product_type': self._get_product_type(sku),
                'towel_color': self._extract_color_from_sku(sku),
                'thread_color': self._extract_thread_color(block),
                'customization_text': self._extract_customization_text(block),
                'font': self._extract_font(block),
                'quantity': self._extract_quantity(block),
                'gift_message': gift_message,
                'source_file': filename
            }
            
            items.append(item)
        
        return items
    
    def _extract_buyer_name(self, text):
        """Extract buyer name from order text"""
        # Look for name pattern at start of text or after "Ship to:"
        patterns = [
            r'Ship to:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "Unknown Buyer"
    
    def _extract_gift_message(self, text):
        """Extract gift message from order text"""
        pattern = r'(?i)Gift\s*(Message|Card|Bag)\s*:\s*(.+?)(?=\n\n|\n[A-Z]|$)'
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            message = match.group(2).strip()
            # Clean up the message
            message = re.sub(r'\s+', ' ', message)
            return message[:200]  # Limit length
        
        return None
    
    def _get_product_type(self, sku):
        """Get product type from SKU prefix"""
        for prefix, product_type in self.PRODUCT_TYPES.items():
            if sku.startswith(prefix):
                return product_type
        return "Unknown Product"
    
    def _extract_color_from_sku(self, sku):
        """Extract towel color from SKU"""
        color_match = re.search(r'-([A-Z][a-z]+)$', sku)
        if color_match:
            return color_match.group(1)
        return "Unknown"
    
    def _extract_thread_color(self, block):
        """Extract thread color from customization block"""
        patterns = [
            r'Thread Color:\s*([A-Za-z]+)',
            r'Thread:\s*([A-Za-z]+)',
            r'Color:\s*([A-Za-z]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, block)
            if match:
                return match.group(1).strip()
        
        return "Not Specified"
    
    def _extract_customization_text(self, block):
        """Extract customization text (names/text to embroider)"""
        patterns = [
            r'(?:Customization|Text|Name):\s*(.+?)(?=\n|Thread|Font|$)',
            r'Embroider:\s*(.+?)(?=\n|Thread|Font|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, block, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                # Clean up
                text = re.sub(r'\s+', ' ', text)
                return text[:100]
        
        return "None"
    
    def _extract_font(self, block):
        """Extract font choice from customization block"""
        pattern = r'(?:Choose Your Font|Font):\s*([A-Za-z\s]+?)(?=\n|Thread|$)'
        match = re.search(pattern, block, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        return "Default"
    
    def _extract_quantity(self, block):
        """Extract quantity from block"""
        pattern = r'Quantity:\s*(\d+)'
        match = re.search(pattern, block)
        
        if match:
            return int(match.group(1))
        
        return 1


class LabelGenerator:
    """Generates 4x6 labels for manufacturing and gift messages"""
    
    def __init__(self):
        self.label_width = 6 * inch
        self.label_height = 4 * inch
    
    def generate_manufacturing_labels(self, items):
        """Generate 4x6 manufacturing labels for all items"""
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(self.label_width, self.label_height))
        
        for item in items:
            self._draw_manufacturing_label(c, item)
            c.showPage()
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _draw_manufacturing_label(self, c, item):
        """Draw a single manufacturing label"""
        x_margin = 0.3 * inch
        y = self.label_height - 0.4 * inch
        line_height = 0.3 * inch
        
        # Title
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, "PRODUCTION LABEL")
        y -= line_height * 1.5
        
        # Order details
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x_margin, y, f"Order ID:")
        c.setFont("Helvetica", 11)
        c.drawString(x_margin + 1.2*inch, y, item['order_id'])
        y -= line_height
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x_margin, y, f"Customer:")
        c.setFont("Helvetica", 11)
        c.drawString(x_margin + 1.2*inch, y, item['buyer_name'][:30])
        y -= line_height * 1.2
        
        # Product details
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, f"Product:")
        c.setFont("Helvetica", 12)
        product_text = f"{item['product_type']} - {item['towel_color']}"
        c.drawString(x_margin + 1.2*inch, y, product_text)
        y -= line_height
        
        # Thread color in Spanish
        thread_color_es = OrderParser.THREAD_COLORS_ES.get(
            item['thread_color'], 
            item['thread_color']
        )
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x_margin, y, f"Thread Color:")
        c.setFont("Helvetica", 11)
        c.drawString(x_margin + 1.5*inch, y, f"{thread_color_es} ({item['thread_color']})")
        y -= line_height
        
        # Customization text
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x_margin, y, f"Customization:")
        y -= line_height * 0.8
        c.setFont("Helvetica", 10)
        # Wrap text if needed
        custom_lines = simpleSplit(item['customization_text'], "Helvetica", 10, 
                                   self.label_width - 2*x_margin)
        for line in custom_lines[:3]:  # Max 3 lines
            c.drawString(x_margin + 0.2*inch, y, line)
            y -= line_height * 0.7
        
        y -= line_height * 0.3
        
        # Font
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_margin, y, f"Font:")
        c.setFont("Helvetica", 10)
        c.drawString(x_margin + 0.7*inch, y, item['font'])
        y -= line_height
        
        # Quantity
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, f"QUANTITY:")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin + 1.5*inch, y, f"{item['quantity']}")
        
        # Footer
        c.setFont("Helvetica", 8)
        c.drawString(x_margin, 0.2*inch, f"Source: {item['source_file']}")
    
    def generate_gift_labels(self, items):
        """Generate 4x6 gift message labels"""
        # Filter items with gift messages
        gift_items = [item for item in items if item.get('gift_message')]
        
        if not gift_items:
            return None
        
        buffer = BytesIO()
        # Portrait orientation for gift labels
        c = canvas.Canvas(buffer, pagesize=(self.label_height, self.label_width))
        
        for item in gift_items:
            self._draw_gift_label(c, item)
            c.showPage()
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _draw_gift_label(self, c, item):
        """Draw a single gift message label (portrait, centered, italic)"""
        width = self.label_height
        height = self.label_width
        
        margin = 0.5 * inch
        max_width = width - 2 * margin
        
        # Center the gift message
        c.setFont("Helvetica-Oblique", 12)
        
        # Split message into lines
        message = item['gift_message']
        lines = simpleSplit(message, "Helvetica-Oblique", 12, max_width)
        
        # Calculate starting Y position to center text vertically
        total_height = len(lines) * 0.25 * inch
        y_start = (height + total_height) / 2
        
        # Draw each line centered
        for line in lines:
            text_width = c.stringWidth(line, "Helvetica-Oblique", 12)
            x = (width - text_width) / 2
            c.drawString(x, y_start, line)
            y_start -= 0.25 * inch
        
        # Add small footer
        c.setFont("Helvetica", 8)
        footer = f"Order: {item['order_id']}"
        footer_width = c.stringWidth(footer, "Helvetica", 8)
        c.drawString((width - footer_width) / 2, 0.3 * inch, footer)


class ProductionPlanner:
    """Generates production planning summaries"""
    
    def __init__(self):
        pass
    
    def generate_summary(self, items):
        """Generate production planning summary"""
        df = pd.DataFrame(items)
        
        summary = {
            'towel_colors': {},
            'hand_towels': {},
            'bath_towels': {},
            'bath_sheets': {},
            'three_piece_equivalents': 0
        }
        
        for _, item in df.iterrows():
            color = item['towel_color']
            product_type = item['product_type']
            quantity = item['quantity']
            sku_prefix = item['sku'].split('-')[0] + '-' + item['sku'].split('-')[1]
            
            # Count by color
            if color not in summary['towel_colors']:
                summary['towel_colors'][color] = 0
            summary['towel_colors'][color] += quantity
            
            # Calculate 3-piece equivalents
            multiplier = OrderParser.PRODUCTION_MULTIPLIERS.get(sku_prefix, 0)
            summary['three_piece_equivalents'] += quantity * multiplier
            
            # Count special items
            if 'Hand' in product_type:
                if color not in summary['hand_towels']:
                    summary['hand_towels'][color] = 0
                summary['hand_towels'][color] += quantity
            elif 'Bath Towel' in product_type and 'Sheet' not in product_type:
                if color not in summary['bath_towels']:
                    summary['bath_towels'][color] = 0
                summary['bath_towels'][color] += quantity
            elif 'Sheet' in product_type:
                if color not in summary['bath_sheets']:
                    summary['bath_sheets'][color] = 0
                summary['bath_sheets'][color] += quantity
        
        return summary


def main():
    """Main Streamlit application"""
    st.title("🧺 Amazon Towel Order Parser")
    st.markdown("Parse Amazon packing slips, generate labels, and plan production")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload", "📋 Orders", "🏭 Production", "🎁 Gift Labels"])
    
    # TAB 1: Upload
    with tab1:
        st.header("Upload Packing Slips")
        st.markdown("Upload one or more Amazon packing slip PDF files")
        
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Parse PDFs", type="primary"):
                with st.spinner("Parsing PDFs..."):
                    parser = OrderParser()
                    all_orders = []
                    
                    for uploaded_file in uploaded_files:
                        orders = parser.parse_pdf(uploaded_file, uploaded_file.name)
                        all_orders.extend(orders)
                    
                    if all_orders:
                        st.session_state.parsed_data = pd.DataFrame(all_orders)
                        st.success(f"✅ Successfully parsed {len(all_orders)} items from {len(uploaded_files)} file(s)")
                    else:
                        st.error("No orders found in uploaded PDFs")
    
    # TAB 2: Orders
    with tab2:
        st.header("Parsed Orders")
        
        if st.session_state.parsed_data is not None:
            df = st.session_state.parsed_data
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                color_filter = st.multiselect("Filter by Color", 
                                             options=df['towel_color'].unique())
            with col2:
                product_filter = st.multiselect("Filter by Product Type",
                                               options=df['product_type'].unique())
            with col3:
                buyer_filter = st.multiselect("Filter by Buyer",
                                             options=df['buyer_name'].unique())
            
            # Apply filters
            filtered_df = df.copy()
            if color_filter:
                filtered_df = filtered_df[filtered_df['towel_color'].isin(color_filter)]
            if product_filter:
                filtered_df = filtered_df[filtered_df['product_type'].isin(product_filter)]
            if buyer_filter:
                filtered_df = filtered_df[filtered_df['buyer_name'].isin(buyer_filter)]
            
            # Display table
            st.dataframe(
                filtered_df[[
                    'order_id', 'buyer_name', 'product_type', 'towel_color',
                    'thread_color', 'customization_text', 'font', 'quantity', 
                    'gift_message'
                ]],
                use_container_width=True
            )
            
            # Export and Label buttons
            col1, col2 = st.columns(2)
            with col1:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="parsed_orders.csv",
                    mime="text/csv"
                )
            
            with col2:
                if st.button("🏷️ Generate Manufacturing Labels"):
                    with st.spinner("Generating labels..."):
                        label_gen = LabelGenerator()
                        items = filtered_df.to_dict('records')
                        labels_pdf = label_gen.generate_manufacturing_labels(items)
                        
                        st.download_button(
                            label="📥 Download Labels PDF",
                            data=labels_pdf,
                            file_name="manufacturing_labels.pdf",
                            mime="application/pdf"
                        )
                    st.success("✅ Labels generated!")
        else:
            st.info("👆 Upload and parse PDFs in the Upload tab first")
    
    # TAB 3: Production Planning
    with tab3:
        st.header("Production Planning Summary")
        
        if st.session_state.parsed_data is not None:
            df = st.session_state.parsed_data
            planner = ProductionPlanner()
            summary = planner.generate_summary(df.to_dict('records'))
            
            # Display summary
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Towel Colors Summary")
                if summary['towel_colors']:
                    color_df = pd.DataFrame([
                        {'Color': k, 'Total Quantity': v}
                        for k, v in sorted(summary['towel_colors'].items())
                    ])
                    st.dataframe(color_df, use_container_width=True)
                
                st.metric("3-Piece Equivalents", f"{summary['three_piece_equivalents']:.1f}")
            
            with col2:
                if summary['hand_towels']:
                    st.subheader("🤚 Hand Towels")
                    ht_df = pd.DataFrame([
                        {'Color': k, 'Quantity': v}
                        for k, v in sorted(summary['hand_towels'].items())
                    ])
                    st.dataframe(ht_df, use_container_width=True)
                
                if summary['bath_towels']:
                    st.subheader("🛁 Bath Towels")
                    bt_df = pd.DataFrame([
                        {'Color': k, 'Quantity': v}
                        for k, v in sorted(summary['bath_towels'].items())
                    ])
                    st.dataframe(bt_df, use_container_width=True)
                
                if summary['bath_sheets']:
                    st.subheader("🛏️ Bath Sheets")
                    bs_df = pd.DataFrame([
                        {'Color': k, 'Quantity': v}
                        for k, v in sorted(summary['bath_sheets'].items())
                    ])
                    st.dataframe(bs_df, use_container_width=True)
        else:
            st.info("👆 Upload and parse PDFs in the Upload tab first")
    
    # TAB 4: Gift Labels
    with tab4:
        st.header("Gift Message Labels")
        
        if st.session_state.parsed_data is not None:
            df = st.session_state.parsed_data
            gift_items = df[df['gift_message'].notna()].to_dict('records')
            
            if gift_items:
                st.success(f"Found {len(gift_items)} order(s) with gift messages")
                
                # Preview gift messages
                for item in gift_items[:5]:  # Show first 5
                    with st.expander(f"Order {item['order_id']} - {item['buyer_name']}"):
                        st.write(f"**Gift Message:** {item['gift_message']}")
                
                if len(gift_items) > 5:
                    st.info(f"...and {len(gift_items) - 5} more")
                
                # Generate gift labels button
                if st.button("🎁 Generate Gift Labels"):
                    with st.spinner("Generating gift labels..."):
                        label_gen = LabelGenerator()
                        gift_labels_pdf = label_gen.generate_gift_labels(gift_items)
                        
                        if gift_labels_pdf:
                            st.download_button(
                                label="📥 Download Gift Labels PDF",
                                data=gift_labels_pdf,
                                file_name="gift_labels.pdf",
                                mime="application/pdf"
                            )
                            st.success("✅ Gift labels generated!")
            else:
                st.info("No orders with gift messages found")
        else:
            st.info("👆 Upload and parse PDFs in the Upload tab first")


if __name__ == "__main__":
    main()
