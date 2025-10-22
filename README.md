# Amazon Towel Order Parser 🧺

A comprehensive Streamlit application for parsing Amazon packing slip PDFs, extracting customized towel order details, generating manufacturing labels, and creating production planning summaries.

## Features

✅ **PDF Parsing**
- Automatic detection of order boundaries
- Multi-page order handling with continuation page detection
- Extracts: Order ID, Buyer Name, SKU, Colors, Thread Colors, Customization Text, Fonts, Quantities, Gift Messages

✅ **Smart Product Recognition**
- Identifies product types from SKU prefixes (6-Piece Sets, 3-Piece Sets, Hand Towels, Bath Towels, Bath Sheets)
- Extracts towel and thread colors automatically

✅ **Manufacturing Labels (4×6)**
- Professional production labels with all order details
- Thread colors translated to Spanish
- Clear quantity and customization information
- Downloadable PDF format

✅ **Gift Message Labels (4×6)**
- Portrait orientation with centered, italicized text
- Automatically detects gift messages/cards/bags
- One label per gift message

✅ **Production Planning**
- Summarizes towel colors and quantities
- Converts to 3-piece equivalents
- Separate tracking for Hand Towels, Bath Towels, and Bath Sheets

✅ **Data Management**
- Sortable and filterable order table
- CSV export capability
- Multiple PDF batch processing

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Steps

1. **Clone or download the application files**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access the application**
- The browser should automatically open
- If not, navigate to: `http://localhost:8501`

## Usage Guide

### 1. Upload Tab 📤
- Click "Browse files" and select one or more Amazon packing slip PDF files
- Click "Parse PDFs" to process all uploaded files
- Wait for the success message confirming parsed items

### 2. Orders Tab 📋
- View all parsed order items in a structured table
- Use filters to narrow down by:
  - Towel Color
  - Product Type
  - Buyer Name
- **Download CSV**: Export filtered data to CSV format
- **Generate Manufacturing Labels**: Create 4×6 labels for all visible orders

### 3. Production Tab 🏭
- View production planning summary including:
  - Total towel colors and quantities
  - 3-piece set equivalents
  - Separate counts for Hand Towels, Bath Towels, and Bath Sheets
- Use this information for daily production planning

### 4. Gift Labels Tab 🎁
- Automatically shows orders containing gift messages
- Preview gift messages before generating labels
- Click "Generate Gift Labels" to create 4×6 portrait labels
- Download the PDF with all gift message labels

## Extracted Data Fields

| Field | Description |
|-------|-------------|
| Order ID | Unique Amazon order identifier |
| Buyer Name | Customer name |
| SKU | Full product SKU (e.g., Set-6Pcs-White) |
| Product Type | 6-Piece Set, 3-Piece Set, Hand Towel, etc. |
| Towel Color | Extracted from SKU |
| Thread Color | Embroidery thread color |
| Customization Text | Names or text to embroider |
| Font | Selected font for embroidery |
| Quantity | Number of items |
| Gift Message | Gift message/card/bag text (if present) |
| Source File | Original PDF filename |

## Product Type Mapping

| SKU Prefix | Product Type |
|------------|--------------|
| Set-6Pcs | 6-Piece Towel Set |
| Set-3Pcs | 3-Piece Towel Set |
| HT-2Pcs | 2-Piece Hand Towel |
| BT-2Pcs | 2-Piece Bath Towel |
| BS-1Pcs | Bath Sheet |

## Production Equivalents

For production planning, items are converted to 3-piece equivalents:
- **Set-6Pcs**: ×2 (equals 2 three-piece sets)
- **Set-3Pcs**: ×1 (equals 1 three-piece set)
- **Hand Towels**: Counted separately
- **Bath Towels**: Counted separately
- **Bath Sheets**: Listed separately

## Thread Color Translations

Thread colors are automatically translated to Spanish on manufacturing labels:
- White → Blanco
- Black → Negro
- Navy → Azul Marino
- Gray → Gris
- Red → Rojo
- And more...

## Label Specifications

### Manufacturing Labels (4×6)
- **Size**: 6" × 4" (landscape)
- **Content**:
  - Order ID and Customer Name
  - Product Type and Towel Color
  - Thread Color (in Spanish and English)
  - Customization Text (wrapped)
  - Font Selection
  - Quantity (large, bold)
  - Source File Reference

### Gift Labels (4×6)
- **Size**: 4" × 6" (portrait)
- **Content**:
  - Gift message (centered, italic, wrapped)
  - Order ID reference (footer)

## Troubleshooting

### PDFs not parsing correctly
- Ensure PDFs are actual Amazon packing slips
- Check that PDFs contain readable text (not scanned images)
- Verify Order ID format matches: "Order ID: XXX-XXXXXXX-XXXXXXX"

### Missing customization data
- Parser looks for keywords like "Customization:", "Thread Color:", "Font:"
- Ensure packing slip contains these fields

### Labels not generating
- Verify filtered data contains items
- Check that reportlab is properly installed: `pip install --upgrade reportlab`

## File Structure

```
amazon_towel_parser/
├── app.py                     # Main application
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Technical Details

- **Framework**: Streamlit
- **PDF Parsing**: pdfplumber
- **Data Processing**: pandas
- **Label Generation**: reportlab
- **Python Version**: 3.10+

## Future Enhancements (Optional)

- [ ] Airtable integration for order tracking
- [ ] Google Sheets sync
- [ ] Email notifications
- [ ] Barcode/QR code generation
- [ ] Advanced similarity matching for continuation pages

## Support

For issues or questions about the application:
1. Check the Troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure input PDFs match the expected Amazon format

## Version

**Version 1.0** - Full implementation of developer specification

---

Built with ❤️ for efficient towel order processing
