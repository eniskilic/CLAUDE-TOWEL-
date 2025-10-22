# Sample Data Format Guide

## Expected Amazon Packing Slip Format

This document shows the expected format of Amazon packing slips that the parser can process.

## Example Order (Complete)

```
Order ID: 123-4567890-1234567

Ship to:
John Smith
123 Main Street
Apartment 4B
New York, NY 10001

Items:

1. Set-6Pcs-White
   Quantity: 2
   Thread Color: Navy
   Customization: John, Sarah, Michael
   Choose Your Font: Script
   Price: $XX.XX

2. HT-2Pcs-Gray
   Quantity: 1
   Thread Color: Black
   Customization: The Smith Family
   Choose Your Font: Block
   Price: $XX.XX

Gift Message: Happy Anniversary! With love from the kids.

Subtotal: $XX.XX
Shipping: $X.XX
Tax: $X.XX
Total: $XX.XX
```

## Key Elements the Parser Looks For

### 1. Order Identification
- **Order ID:** Format: `Order ID: XXX-XXXXXXX-XXXXXXX`
- **Location:** Usually at the top of first page
- **Important:** Each new order starts with this line

### 2. Buyer Information
- **Ship to:** Followed by name
- **Format:** FirstName LastName
- **Example:** `John Smith`

### 3. SKU Patterns
The parser recognizes these SKU formats:
- `Set-6Pcs-[Color]` → 6-Piece Towel Set
- `Set-3Pcs-[Color]` → 3-Piece Towel Set
- `HT-2Pcs-[Color]` → 2-Piece Hand Towel
- `BT-2Pcs-[Color]` → 2-Piece Bath Towel
- `BS-1Pcs-[Color]` → Bath Sheet

**Color Examples:**
- Set-6Pcs-White
- Set-3Pcs-Navy
- HT-2Pcs-Gray
- BT-2Pcs-Beige
- BS-1Pcs-Brown

### 4. Customization Details
Each item may include:
- **Thread Color:** `Thread Color: [Color]`
- **Customization Text:** `Customization: [Text]` or `Text: [Text]`
- **Font:** `Choose Your Font: [Font Name]`
- **Quantity:** `Quantity: [Number]`

### 5. Gift Messages
Detected by keywords (case-insensitive):
- `Gift Message: [message text]`
- `Gift Card: [message text]`
- `Gift Bag: [message text]`

## Multi-Page Orders

For orders spanning multiple pages:

**Page 1:**
```
Order ID: 123-4567890-1234567
Ship to: Jane Doe
...
Item 1 details
Item 2 details
```

**Page 2 (continuation):**
```
(no Order ID line)
Jane Doe (buyer name continues)
...
Item 3 details
Item 4 details
```

The parser automatically merges continuation pages using buyer name matching.

## Supported Thread Colors

The parser translates these colors to Spanish on labels:
- White → Blanco
- Black → Negro
- Navy → Azul Marino
- Gray → Gris
- Brown → Marrón
- Red → Rojo
- Pink → Rosa
- Blue → Azul
- Green → Verde
- Yellow → Amarillo
- Orange → Naranja
- Purple → Púrpura
- Beige → Beige
- Cream → Crema
- Ivory → Marfil

## Supported Towel Colors

Any capitalized color name in the SKU:
- White
- Navy
- Gray
- Black
- Brown
- Beige
- Red
- Blue
- Green
- Pink
- Yellow
- Orange
- Purple
- Cream
- Ivory

## Supported Fonts

Common font names extracted:
- Script
- Block
- Serif
- Sans Serif
- Cursive
- Modern
- Classic
- Elegant

## Example of Complete Data Extraction

**From this PDF text:**
```
Order ID: 123-4567890-1234567
Ship to: Mary Johnson
Set-6Pcs-White
Quantity: 1
Thread Color: Navy
Customization: Emily, Jack, Sophie
Choose Your Font: Script
Gift Message: For our favorite teacher!
```

**Parser extracts:**
| Field | Value |
|-------|-------|
| Order ID | 123-4567890-1234567 |
| Buyer Name | Mary Johnson |
| SKU | Set-6Pcs-White |
| Product Type | 6-Piece Towel Set |
| Towel Color | White |
| Thread Color | Navy |
| Customization Text | Emily, Jack, Sophie |
| Font | Script |
| Quantity | 1 |
| Gift Message | For our favorite teacher! |

## Testing Your PDFs

Before processing, verify your PDFs contain:
1. ✅ Searchable text (not scanned images)
2. ✅ Clear Order ID on first page of each order
3. ✅ SKU in recognized format
4. ✅ Buyer name in "Ship to:" section
5. ✅ Customization details with clear labels

## Common Issues

❌ **Issue:** Parser doesn't find orders  
✅ **Fix:** Ensure "Order ID:" text is present

❌ **Issue:** Wrong buyer names  
✅ **Fix:** Check "Ship to:" formatting

❌ **Issue:** Missing customization  
✅ **Fix:** Verify field labels (Thread Color:, Customization:, etc.)

❌ **Issue:** Colors not recognized  
✅ **Fix:** Ensure SKU follows pattern: Type-Count-Color

---

This format guide helps ensure your Amazon packing slips are compatible with the parser.
