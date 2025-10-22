# Troubleshooting Guide - Amazon Towel Order Parser

## Installation Issues

### Problem: "command not found: streamlit"
**Cause:** Streamlit not installed or not in PATH

**Solutions:**
1. Install streamlit: `pip install streamlit`
2. Check installation: `pip list | grep streamlit`
3. Try with python: `python -m streamlit run amazon_towel_parser.py`
4. Verify Python installation: `python --version` (should be 3.10+)

### Problem: "No module named 'pdfplumber'"
**Cause:** Missing required package

**Solutions:**
1. Install missing package: `pip install pdfplumber`
2. Install all requirements: `pip install -r requirements.txt`
3. If using virtual environment, activate it first

### Problem: "ModuleNotFoundError: No module named 'reportlab'"
**Cause:** reportlab not installed

**Solutions:**
1. Install reportlab: `pip install reportlab`
2. Try upgrading: `pip install --upgrade reportlab`
3. On some systems: `pip install reportlab[pycairo]`

### Problem: Permission denied when installing packages
**Cause:** Insufficient permissions

**Solutions:**
1. Use `--user` flag: `pip install --user streamlit`
2. Use virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## Application Launch Issues

### Problem: Application won't start
**Cause:** Various potential issues

**Solutions:**
1. Check Python version: `python --version` (need 3.10+)
2. Verify file location: `ls -la app.py`
3. Check for syntax errors: `python -m py_compile app.py`
4. Try: `python -m streamlit run app.py`

### Problem: Port already in use
**Cause:** Another Streamlit app running

**Solutions:**
1. Stop other Streamlit instances
2. Use different port: `streamlit run app.py --server.port 8502`
3. Find and kill process using port 8501

### Problem: Browser doesn't open automatically
**Cause:** Browser launch issue

**Solutions:**
1. Manually navigate to: `http://localhost:8501`
2. Check terminal for actual URL
3. Try: `streamlit run app.py --server.headless false`

---

## PDF Parsing Issues

### Problem: "No orders found in uploaded PDFs"
**Cause:** PDFs don't match expected format or are image-based

**Solutions:**
1. ✅ Verify PDF contains searchable text (try copying text from PDF)
2. ✅ Check "Order ID:" is present in format: `Order ID: XXX-XXXXXXX-XXXXXXX`
3. ✅ Ensure PDF is Amazon packing slip, not invoice
4. ✅ Try with a different PDF to isolate issue
5. ✅ Check if PDF is password protected

### Problem: Wrong number of items extracted
**Cause:** SKU format not recognized or duplicate detection

**Solutions:**
1. ✅ Verify SKU format: `[Type]-[Count]-[Color]`
   - Valid: `Set-6Pcs-White`, `HT-2Pcs-Navy`
   - Invalid: `6PCS-SET-WHITE`, `HandTowel-Navy`
2. ✅ Check for multiple items with same SKU
3. ✅ Look for quantity field: `Quantity: N`

### Problem: Buyer name showing as "Unknown Buyer"
**Cause:** Name format not recognized

**Solutions:**
1. ✅ Check for "Ship to:" line followed by name
2. ✅ Name should be: FirstName LastName (capitalized)
3. ✅ Verify name appears near top of document
4. ✅ Try PDFs from different orders to confirm pattern

### Problem: Missing customization details
**Cause:** Field labels not matching expected patterns

**Solutions:**
1. ✅ Verify these field names in PDF:
   - "Thread Color:" or "Thread:"
   - "Customization:" or "Text:" or "Embroider:"
   - "Choose Your Font:" or "Font:"
2. ✅ Check spelling and capitalization
3. ✅ Ensure details are within 500 characters after SKU
4. ✅ Look for line breaks interrupting field text

### Problem: Gift messages not detected
**Cause:** Gift message format not recognized

**Solutions:**
1. ✅ Verify PDF contains: "Gift Message:", "Gift Card:", or "Gift Bag:"
2. ✅ Check message appears after these keywords
3. ✅ Try case variations (should work with any case)
4. ✅ Ensure message is on same or next line

### Problem: Multi-page orders not merging
**Cause:** Continuation pages not detected

**Solutions:**
1. ✅ Ensure continuation pages DON'T have "Order ID:" line
2. ✅ Verify buyer name appears on continuation pages
3. ✅ Check if buyer name format matches exactly
4. ✅ Currently uses basic name matching (90% threshold planned)

---

## Data Display Issues

### Problem: Table shows wrong data
**Cause:** Parsing error or display issue

**Solutions:**
1. Re-upload and re-parse PDFs
2. Clear browser cache
3. Check source PDF manually
4. Download CSV to verify raw data

### Problem: Filters not working
**Cause:** Data type mismatch or empty filters

**Solutions:**
1. Ensure you've selected filter values
2. Clear filters and try again
3. Refresh page (Ctrl+R)
4. Check if filtered field contains null values

### Problem: Cannot download CSV
**Cause:** Browser download settings

**Solutions:**
1. Check browser download location
2. Allow downloads in browser settings
3. Try different browser
4. Verify data exists in table

---

## Label Generation Issues

### Problem: Labels PDF is blank
**Cause:** reportlab rendering issue or empty dataset

**Solutions:**
1. Verify orders are displayed in Orders tab
2. Check filters aren't hiding all data
3. Update reportlab: `pip install --upgrade reportlab`
4. Try generating for single order first

### Problem: Text cutoff on labels
**Cause:** Text too long for label space

**Solutions:**
1. This is expected for very long customization text
2. Labels wrap text to 3 lines maximum
3. Edit source data if critical
4. Font size automatically adjusted

### Problem: Spanish translations missing
**Cause:** Color not in translation dictionary

**Solutions:**
1. English name still shows
2. Add to THREAD_COLORS_ES in code if needed
3. Common colors are pre-loaded

### Problem: Gift labels in wrong orientation
**Cause:** By design - gift labels are portrait

**Solutions:**
1. This is intentional (4"×6" portrait)
2. Manufacturing labels are 6"×4" landscape
3. Print settings may need adjustment

### Problem: Labels won't download
**Cause:** PDF generation failed or browser issue

**Solutions:**
1. Check browser console for errors
2. Try different browser
3. Verify reportlab installed correctly
4. Check for sufficient memory (large batch)

---

## Production Planning Issues

### Problem: Wrong 3-piece equivalents
**Cause:** Calculation issue or unexpected product type

**Solutions:**
1. Verify conversion rules:
   - Set-6Pcs × 2 = 2 three-piece sets
   - Set-3Pcs × 1 = 1 three-piece set
   - HT, BT, BS = counted separately
2. Check SKU format matches exactly
3. Review individual items in Orders tab

### Problem: Colors not grouping correctly
**Cause:** Color name variations

**Solutions:**
1. Check SKU color spelling (case-sensitive)
2. Verify colors extracted correctly in Orders tab
3. Color comes from SKU, not customization field

---

## Performance Issues

### Problem: Slow PDF parsing
**Cause:** Large or complex PDFs

**Solutions:**
1. Process files in smaller batches
2. Use PDFs with text layer (not scanned)
3. Reduce number of simultaneous uploads
4. Expected: ~1-5 seconds per PDF page

### Problem: Application becomes unresponsive
**Cause:** Memory issue or large dataset

**Solutions:**
1. Restart application
2. Process smaller batches
3. Clear session state (refresh page)
4. Check system memory

### Problem: Browser crashes
**Cause:** Too much data displayed at once

**Solutions:**
1. Use filters to reduce visible rows
2. Export CSV and use external tool for large datasets
3. Process in smaller batches
4. Increase browser memory limit

---

## Data Quality Issues

### Problem: Inconsistent quantity values
**Cause:** Quantity field format variations

**Solutions:**
1. Parser looks for "Quantity: N"
2. Defaults to 1 if not found
3. Verify format in source PDF
4. Manually verify in Orders tab

### Problem: Wrong product types
**Cause:** SKU prefix not recognized

**Solutions:**
1. Check SKU format exactly matches:
   - Set-6Pcs, Set-3Pcs, HT-2Pcs, BT-2Pcs, BS-1Pcs
2. Verify hyphen placement
3. Case-sensitive (use exact capitalization)

### Problem: Font showing as "Default"
**Cause:** Font field not found

**Solutions:**
1. Check for "Choose Your Font:" in PDF
2. Verify spacing and colon
3. Default is used when not specified
4. This is normal for items without font selection

---

## Common Error Messages

### "Error parsing [filename]: [error]"
**Meaning:** PDF parsing failed

**Action:** Check PDF format and try again

### "pdfplumber.pdf.PDFSyntaxError"
**Meaning:** Corrupted or invalid PDF

**Action:** Re-download or re-export PDF

### "FileNotFoundError"
**Meaning:** File path incorrect

**Action:** Verify file location and permissions

### "PermissionError"
**Meaning:** Cannot write output file

**Action:** Check folder permissions or choose different location

---

## Getting Help

### Before Asking for Help
1. ✅ Check this troubleshooting guide
2. ✅ Verify Python version (3.10+)
3. ✅ Confirm all dependencies installed
4. ✅ Test with a different PDF
5. ✅ Review error messages carefully

### What to Include When Reporting Issues
- Python version: `python --version`
- Package versions: `pip list | grep -E "streamlit|pdfplumber|pandas|reportlab"`
- Error message (full text)
- Sample PDF (if possible, redacted)
- Steps to reproduce

### Quick Diagnostics
Run these commands and share output:
```bash
python --version
pip list | grep streamlit
pip list | grep pdfplumber
pip list | grep reportlab
pip list | grep pandas
```

---

## Prevention Tips

✅ **Best Practices:**
1. Keep packages updated: `pip install --upgrade -r requirements.txt`
2. Use virtual environment for isolation
3. Backup parsed CSV files regularly
4. Test with sample PDF before batch processing
5. Verify data quality in Orders tab before generating labels
6. Save label PDFs immediately after generation

✅ **Quality Checks:**
1. Spot-check first few parsed orders
2. Verify buyer names are correct
3. Confirm quantities match source
4. Check that all customizations are captured
5. Review gift messages for accuracy

---

**Still having issues?** Double-check the SAMPLE_DATA_FORMAT.md to ensure your PDFs match the expected format.
