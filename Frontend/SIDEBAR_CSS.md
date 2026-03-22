# Sidebar CSS - Clean & Lightweight

## Overview
Refined sidebar UI with improved spacing, alignment, and subtle interactions. No shadows or bright highlights.

---

## Key Changes

### **1. Container & Spacing**
```css
[data-testid="stSidebar"] {
    background: var(--primary);  /* #0F172A - Deep navy */
}

[data-testid="stSidebar"] > div {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}
```
- Consistent padding for breathing room
- No shadows or excessive borders

---

### **2. Header (Brand Section)**
```css
[data-testid="stSidebar"] h1 {
    font-size: 30px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin: 0 0 4px 0;
    color: var(--text-primary);
}

[data-testid="stSidebar"] > div > div:first-child > div:first-child em {
    font-size: 15px;
    opacity: 0.7;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    font-weight: 500;
}
```
- Bold header with tight letter spacing
- Subtitle in uppercase with reduced opacity (not font-weight)

---

### **3. Section Dividers**
```css
[data-testid="stSidebar"] hr {
    margin: 18px 0;
    opacity: 0.4;        /* Using opacity, not bright color */
}
```
- Increased vertical spacing (18px)
- Subtle 40% opacity instead of bright dividers

---

### **4. Section Headers**
```css
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    margin: 18px 0 12px 0;
    color: var(--text-secondary);
    opacity: 0.9;
}
```
- Uppercase labels for clarity
- Subtle gray color with high opacity
- Proper margins for visual hierarchy

---

### **5. Buttons - Lightweight**
```css
[data-testid="stSidebar"] button {
    background: rgba(255, 255, 255, 0.04) !important;
    color: var(--text-primary) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: var(--radius) !important;
    font-size: 15px;
    font-weight: 500;
    padding: 8px 12px !important;
    margin: 6px 0 !important;
    transition: var(--transition);
}

/* Hover - Uses opacity & font-weight */
[data-testid="stSidebar"] button:hover {
    background: rgba(255, 255, 255, 0.08) !important;    /* Opacity increase */
    color: var(--accent-light) !important;                /* Subtle color shift */
    font-weight: 600;                                      /* Font-weight boost */
}

/* Active - Visual feedback */
[data-testid="stSidebar"] button:active {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: var(--accent) !important;
}
```

**Features:**
- ✅ Minimal background (0.04 opacity)
- ✅ Subtle border (0.06 opacity)
- ✅ Hover uses opacity + font-weight (not bright highlight)
- ✅ Active state shows accent border
- ✅ No shadows

---

### **6. Checkboxes & Labels**
```css
[data-testid="stSidebar"] label {
    font-size: 15px;
    font-weight: 400;
    color: var(--text-primary);
    margin: 8px 0;
    cursor: pointer;
    opacity: 0.95;
}

[data-testid="stSidebar"] label:hover {
    opacity: 1;              /* Opacity increase */
    font-weight: 500;        /* Font-weight increase */
}
```

**Interaction Pattern:**
- Base: 95% opacity, weight 400
- Hover: 100% opacity, weight 500
- No color changes, uses opacity + weight

---

### **7. Select Box (Dropdown)**
```css
[data-testid="stSidebar"] [role="listbox"],
[data-testid="stSidebar"] [role="combobox"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius) !important;
}

[data-testid="stSidebar"] [role="listbox"]:focus,
[data-testid="stSidebar"] [role="combobox"]:focus {
    border-color: var(--accent) !important;
    box-shadow: none !important;                         /* No box-shadow */
}
```
- Minimal background
- Focus shows accent border only

---

### **8. Expanders - Clean**
```css
[data-testid="stSidebar"] .streamlit-expander {
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: var(--radius) !important;
    margin: 8px 0 !important;
}

[data-testid="stSidebar"] .streamlit-expander:hover {
    border-color: rgba(255, 255, 255, 0.1) !important;   /* Opacity increase */
    background: rgba(255, 255, 255, 0.02) !important;    /* Subtle bg shift */
}

[data-testid="stSidebar"] [data-testid="stExpanderToggleIcon"] {
    opacity: 0.6;
    transition: var(--transition);
}

[data-testid="stSidebar"] .streamlit-expander:hover [data-testid="stExpanderToggleIcon"] {
    opacity: 1;              /* Opacity increase */
    font-weight: 600;        /* Weight increase */
}
```

**Hover Pattern:**
- Border opacity: 0.05 → 0.1
- Background: 0 → 0.02 opacity
- Icon opacity: 0.6 → 1.0

---

### **9. Lists in Sidebar**
```css
[data-testid="stSidebar"] ul {
    list-style: none;
    padding-left: 0;
}

[data-testid="stSidebar"] li {
    padding-left: 0;
    margin: 6px 0;
    font-size: 13px;
    color: var(--text-primary);
}

[data-testid="stSidebar"] li::before {
    content: "• ";
    color: var(--accent);
    margin-right: 6px;
    opacity: 0.6;            /* Subtle bullet points */
}
```
- Clean list without default bullets
- Accent-colored bullets with 60% opacity

---

### **10. Info Boxes & Alerts**
```css
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: var(--radius) !important;
    padding: 10px 12px !important;
    margin: 8px 0 !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] > div {
    font-size: 15px;
    color: var(--text-secondary) !important;
}
```
- Minimal visual weight
- Subtle border and background
- Smaller text size

---

### **11. Typography - Optimized**
```css
[data-testid="stSidebar"] p {
    font-size: 15px;
    line-height: 1.5;
    color: var(--text-primary);
    margin: 8px 0;
}

[data-testid="stSidebar"] small {
    font-size: 11px;
    color: var(--text-secondary);
    opacity: 0.8;
}
```
- 13px base for readability
- Secondary text uses opacity

---

## Interaction Patterns

| Element | Default | Hover | Active |
|---------|---------|-------|--------|
| **Button** | 4% opacity bg | 8% opacity, accent text, weight 600 | 10% opacity, accent border |
| **Label** | 95% opacity, weight 400 | 100% opacity, weight 500 | N/A |
| **Link** | 85% opacity | 100% opacity, weight 500 | N/A |
| **Expander** | 5% border | 10% border, 2% bg | N/A |
| **Icon** | 60% opacity | 100% opacity | N/A |

---

## Color Scheme

```
Background:           #0F172A (--primary)
Text Primary:         #F1F5F9
Text Secondary:       #CBD5E1
Accent:               #3B82F6
Accent Light:         #60A5FA
Border:               rgba(255,255,255, 0.05-0.1)
Button Background:    rgba(255,255,255, 0.04-0.1)
```

---

## Design Principles

✅ **No Shadows** - Only subtle opacity changes
✅ **No Bright Highlights** - Uses opacity instead of color
✅ **Font-Weight for Emphasis** - 400→500→600 for interaction
✅ **Opacity Transitions** - 0.6→0.8→1.0 for states
✅ **Clean Spacing** - 6-18px margins between elements
✅ **Consistent Radius** - 6px border-radius throughout
✅ **Icon/Text Alignment** - Proper margins and spacing
✅ **Visual Noise Reduction** - Minimal borders, subtle colors

---

## Files Modified

- ✅ `app.py` - All sidebar CSS rules added
