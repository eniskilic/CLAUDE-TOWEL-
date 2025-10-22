# Quick Start Guide - Amazon Towel Order Parser

## Get Started in 3 Steps

### Step 1: Install Dependencies ⚙️

Open your terminal/command prompt and run:

```bash
pip install streamlit pdfplumber pandas reportlab
```

**OR** use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Launch the Application 🚀

In the same directory as `app.py`, run:

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

### Step 3: Process Your Orders 📄

1. **Upload PDFs**
   - Click on the "Upload" tab
   - Select one or more Amazon packing slip PDF files
   - Click "Parse PDFs"

2. **View Orders**
   - Go to the "Orders" tab
   - See all parsed orders in a table
   - Filter by color, product type, or buyer
   - Download CSV or generate manufacturing labels

3. **Check Production**
   - Go to the "Production" tab
   - View summary of all towel colors
   - See 3-piece equivalents for planning

4. **Generate Gift Labels** (if applicable)
   - Go to the "Gift Labels" tab
   - Review orders with gift messages
   - Generate 4×6 gift labels

## What You Need

✅ Python 3.10 or higher installed  
✅ Amazon packing slip PDFs  
✅ Internet connection (for first-time package installation)

## Expected PDF Format

Your PDFs should contain Amazon packing slips with:
- Order ID (format: Order ID: XXX-XXXXXXX-XXXXXXX)
- Buyer name and address
- SKU (e.g., Set-6Pcs-White, HT-2Pcs-Navy)
- Customization details:
  - Thread Color
  - Customization Text/Names
  - Font choice
- Optional: Gift Message/Card/Bag

## Common Commands

**Start the app:**
```bash
streamlit run app.py
```

**Stop the app:**
- Press `Ctrl+C` in the terminal

**Restart the app:**
- Stop it (Ctrl+C)
- Run the start command again

**Update packages:**
```bash
pip install --upgrade streamlit pdfplumber pandas reportlab
```

## First-Time Setup Checklist

- [ ] Python 3.10+ installed
- [ ] Downloaded all application files
- [ ] Installed required packages
- [ ] Have Amazon packing slip PDFs ready
- [ ] Ran `streamlit run app.py`
- [ ] Browser opened to http://localhost:8501

## Tips for Best Results

💡 **Multiple PDFs**: Upload all PDFs at once for batch processing  
💡 **Filters**: Use the filter options to focus on specific colors or buyers  
💡 **Labels**: Generate labels only for filtered items to save paper  
💡 **CSV Export**: Download CSV for backup or external analysis  
💡 **Production Planning**: Check the Production tab daily to plan manufacturing

## Next Steps

Once you're comfortable with the basics:

1. Explore the filtering options in the Orders tab
2. Experiment with different label batches
3. Use production summaries for capacity planning
4. Export CSV data for record-keeping

## Need Help?

**Problem**: PDFs won't parse  
**Solution**: Ensure PDFs contain searchable text (not scanned images)

**Problem**: Missing customization data  
**Solution**: Check that packing slip includes customization fields

**Problem**: Labels look wrong  
**Solution**: Verify the PDF parsing extracted correct data in Orders tab

**Problem**: Application won't start  
**Solution**: Check that all dependencies installed: `pip list | grep -E "streamlit|pdfplumber|pandas|reportlab"`

---

Happy processing! 🎉
