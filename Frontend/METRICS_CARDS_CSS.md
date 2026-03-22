# Key Metrics Cards - CSS Styles

## Card Structure - Data-Focused

### **Card Container**
```css
/* Clean white/transparent background - softened contrast */
background: rgba(255, 255, 255, 0.04);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 6px;
padding: 20px;

/* Hover only - subtle transition */
:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.12);
}
```

**Features:**
- ✅ Soft white background (4% opacity) - calm visual presence
- ✅ Minimal border (8% opacity)
- ✅ No shadows
- ✅ Hover-only animation (background + border)
- ✅ 20px padding for breathing room

---

## Typography Hierarchy - Number First

### **1. Metric Value (Dominant)**
```css
font-size: 28px;
font-weight: 700;           /* Bold and serious */
letter-spacing: -0.7px;     /* Tight for emphasis */
line-height: 1.1;
margin-bottom: 6px;
```

- Large, clear number reads first
- High contrast color (accent only)
- Negative letter-spacing for premium look

### **2. Unit (Supporting)**
```css
font-size: 16px;
font-weight: 500;
opacity: 0.8;
margin-left: 4px;           /* Inline with value */
```

- Smaller than value, inline positioning
- Not overwhelming the number

### **3. Label (Secondary)**
```css
font-size: 12px;
font-weight: 500;
letter-spacing: 0.5px;
text-transform: uppercase;
color: #CBD5E1;             /* Muted gray */
opacity: 0.8;
margin-bottom: 8px;
```

- Uppercase for serious tone
- Small and restrained
- Secondary information, below number

### **4. Trend Indicator (Subtle)**
```css
font-size: 11px;
font-weight: 500;
opacity: 0.8;
margin-top: 8px;
```

- Minimal text size
- One accent color for trend direction
- Below label for visual hierarchy

---

## Hierarchy Flow

```
┌────────────────────────┐
│  28px Bold Accent Text │  ← Number (dominates)
│  16px Unit             │
│                        │  (6px gap)
│  12px GRAY LABEL       │  ← Label (secondary)
│  11px Trend Text       │  ← Trend (subtle)
└────────────────────────┘
```

**Key:** Number > Unit > Label > Trend

---

## Color Usage - One Accent Max

| Element | Color | Usage |
|---------|-------|-------|
| Number | `{accent}` | One color per metric (blue, green, red, etc.) |
| Unit | Accent (0.8 opacity) | Subtle support |
| Label | #CBD5E1 (0.8 opacity) | Muted gray |
| Trend | Accent matching trend | Color matches metric or trend |
| Background | rgba(255,255,255,0.04) | Calm, barely visible |
| Border | rgba(255,255,255,0.08) | Minimal definition |

---

## Spacing & Alignment

| Element | Margin | Padding |
|---------|--------|---------|
| Card | 10px bottom | 20px all |
| Value | 6px bottom | — |
| Label | 8px bottom | — |
| Trend | 8px top | — |
| Unit | 4px left | — |

---

## Interactions - Hover Only

**No animations on load** - cards appear instantly

**On hover:**
- Background opacity: 4% → 6%
- Border opacity: 8% → 12%
- Transition: 0.2s ease (smooth, not jarring)

---

## Data-Focused Design Rules

✅ **Number First** - 28px dominates the card
✅ **Calm Presence** - Soft white background (4% opacity)
✅ **One Accent** - Only one color per card
✅ **Serious Tone** - Uppercase labels, bold weights
✅ **Clear Hierarchy** - Value → Unit → Label → Trend
✅ **Minimal Interaction** - Hover-only changes
✅ **No Animation** - Cards appear instantly, hover only
✅ **Proper Spacing** - 6-8px gaps for readability

---

## CSS Rules Applied

**HTML-based cards** (from components.py):
- 28px font for values (up from 26px)
- 6px margin between value and label (cleaner)
- 20px padding (more breathing room)
- rgba(255,255,255,0.04) background (softer white)
- Hover state with background + border shift

**Streamlit metrics** (if using st.metric):
- Override default styling with same rules
- 32px font size for values
- Clean borders and backgrounds
- Proper spacing for label placement

---

## Files Modified

- ✅ `components.py` - HTML card structure simplified
- ✅ `app.py` - CSS rules for card styling + hover effects
