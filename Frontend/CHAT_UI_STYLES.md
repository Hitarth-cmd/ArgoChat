# AgroChat Chat UI - CSS Styles

## Overview
Professional chat interface with clean, readable design. No cartoon styles, avatars, or excessive borders.

---

## Chat Message Styling

### **User Messages**
```css
/* Clean blue rectangles with subtle gradient */
.user-bubble {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    color: #FFFFFF;
    padding: 12px 18px;
    border-radius: 6px;
    max-width: 100%;                    /* Prevents long single lines */
    font-size: 14px;
    line-height: 1.6;                  /* Easy to read */
    box-shadow: 0 1px 2px rgba(59, 130, 246, 0.12);
    transition: all 0.2s ease;
}

.user-bubble:hover {
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.18);
    transform: translateY(-1px);
}
```

**Features:**
- ✅ Soft gradient for visual interest (not flashy)
- ✅ Readable 14px size with 1.6 line-height
- ✅ 65% max-width prevents awkward long lines
- ✅ Subtle shadow and hover effect
- ✅ Right-aligned with Flexbox

---

### **Bot Messages**
```css
/* Soft muted background with minimal visual weight */
.bot-bubble {
    background: rgba(255, 255, 255, 0.02);     /* Almost transparent */
    color: #F1F5F9;                             /* Clean white text */
    padding: 12px 30px;
    border-radius: 6px;
    max-width: 65%;                             /* Same width as user */
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: all 0.2s ease;
}

.bot-bubble:hover {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
    background: rgba(255, 255, 255, 0.03);
}
```

**Features:**
- ✅ Minimal visual weight (barely visible background)
- ✅ Subtle border for definition (not heavy)
- ✅ Hover effect for interactivity
- ✅ Left-aligned with Flexbox
- ✅ Identical width to user messages

---

### **Message Containers (Animation)**
```css
/* User message wrapper - right alignment + animation */
.chat-message-user {
    display: flex;
    justify-content: flex-end;
    margin: 12px 0;
    animation: slideInRight 0.3s ease-out;
}

/* Bot message wrapper - left alignment + animation */
.chat-message-bot {
    display: flex;
    justify-content: flex-start;
    margin: 12px 0;
    animation: slideInLeft 0.3s ease-out;
}

/* Subtle slide-in animations */
@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-12px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(12px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
```

**Features:**
- ✅ Clear left/right separation
- ✅ 12px margin between messages
- ✅ Subtle fade + slide animation (not distracting)
- ✅ No avatars or excessive padding

---

### **Timestamps**
```css
.message-time {
    font-size: 11px;
    color: #CBD5E1;                 /* Soft gray */
    margin-top: 6px;
    opacity: 0.7;
    letter-spacing: 0.3px;
}

.user-time {
    text-align: right;
    padding-right: 2px;
}

.bot-time {
    text-align: left;
    padding-left: 2px;
}
```

---

## Supporting Elements

### **Typography**
```css
h1 { font-size: 28px; font-weight: 600; letter-spacing: -0.5px; }
h2 { font-size: 20px; font-weight: 600; letter-spacing: -0.3px; }
h3 { font-size: 16px; font-weight: 500; }

strong { font-weight: 600; }
em { color: #CBD5E1; font-style: italic; }
```

### **Code Blocks**
```css
code {
    background: rgba(255, 255, 255, 0.04);
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 13px;
    color: #A8E6CF;
    font-family: 'Menlo', 'Monaco', monospace;
}

pre {
    background: rgba(15, 23, 42, 0.8);
    padding: 12px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
```

### **Lists**
```css
ul, ol {
    margin: 8px 0;
    padding-left: 20px;
}

li {
    margin: 6px 0;
    color: #F1F5F9;
}
```

### **Links**
```css
a {
    color: #3B82F6;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: all 0.2s ease;
}

a:hover {
    border-bottom-color: #3B82F6;
}
```

### **Blockquotes**
```css
blockquote {
    border-left: 3px solid #3B82F6;
    padding-left: 12px;
    margin: 12px 0;
    color: #CBD5E1;
    font-style: italic;
}
```

---

## Color Palette

| Element | Color | Usage |
|---------|-------|-------|
| User Message | #3B82F6 → #2563EB | Primary messages |
| Bot Message | rgba(255,255,255,0.02) | Secondary messages |
| Text Primary | #F1F5F9 | Main text |
| Text Secondary | #CBD5E1 | Subtle text, timestamps |
| Accent | #3B82F6 | Links, highlights |
| Background | #0F172A | Page background |
| Border | rgba(255,255,255,0.05) | Subtle dividers |

---

## Key Design Decisions

✅ **Max-width 65%** - Prevents awkward long lines, improves readability
✅ **Soft Gradient** - User messages have gentle blue gradient (not flat)
✅ **Minimal Bot Bubble** - Transparent background blends with interface
✅ **Soft Corners** - 6px border-radius (not circular, not sharp)
✅ **Subtle Shadows** - 1px blur for depth, not heavy (0.08-0.12 opacity)
✅ **Slide Animation** - 0.3s fade + 12px translate (not jarring)
✅ **No Borders** - Only subtle 1px on bot message, no cartoonish speech bubbles
✅ **Clean Alignment** - Flexbox with proper spacing and margins
✅ **Muted Colors** - Dark theme with refined palette (no neon)
✅ **Readable Typography** - 14px base, 1.6 line-height, proper letter spacing

---

## Files Modified

- ✅ `app.py` - All CSS styles + message rendering functions

---

## Usage

Messages automatically apply styles through CSS classes:
- User messages: `.user-bubble` wrapped in `.chat-message-user`
- Bot messages: `.bot-bubble` wrapped in `.chat-message-bot`
- Timestamps: `.message-time` with `.user-time` or `.bot-time`
