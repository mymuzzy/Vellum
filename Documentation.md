Welcome to the Vellum documentation! This guide covers everything you need to get Vellum running and mastering its secure, offline workflow.

---

## 1. Installation

Vellum runs fully offline. You just need Python 3.x and a few libraries. 

### Step 1: Install Ghostscript (Optional but Highly Recommended)
Vellum has a built-in Python compressor, but for the absolute *best* compression results, Ghostscript is recommended. 
* **macOS:** `brew install ghostscript`
* **Linux (Ubuntu/Debian):** `sudo apt install ghostscript`
* **Windows:** Download the installer from the [Ghostscript website](https://ghostscript.com/) (or use `winget install Ghostscript.Ghostscript`) and ensure it is added to your system PATH.

### Step 2: Setup Vellum
Open your terminal or command prompt and run:

```bash
# Clone the project
git clone https://github.com/mymuzzy/vellum.git
cd vellum

# Create and activate a virtual environment
python3 -m venv pdf_tool_env
source pdf_tool_env/bin/activate   # On Windows use: pdf_tool_env\Scripts\activate

# Install all required libraries in one go
python3 -m pip install PyQt6 PyMuPDF pypdf reportlab

# Launch Vellum
python3 main.py
```

---

## 2. The Interface 

Vellum is built around a clean, distraction-free **3-Panel Layout**:

* **Left Panel (The Toolbox):** All your editing tools are fully expanded here. No hidden menus.
* **Middle Panel (The Canvas):** Your document viewport. Scroll through your PDF, and click on any page to select/deselect it. 
* **Right Panel (The Control Room):** Displays real-time file stats, Zoom controls, your Undo history, and Export settings.

---

## 3. The Tool Kit: How to Use Them

Here is a quick breakdown of every tool in your left panel and how to use them effectively:

**Unlock & Decrypt**
Got a password-protected PDF? Just drag and drop it in. Vellum will automatically detect the encryption and prompt you for the password. Enter it, click decrypt, and Vellum instantly creates a secure, unlocked temporary copy for you to edit or merge. 

**Merge PDFs**
When you open this tool, the UI shifts to give you full screen space. You can drag and drop multiple PDF files into the list. Use the up and down arrow buttons to perfectly reorder your files. Once sorted, hit the merge button, and it instantly loads the combined document into your main viewport.

**Split Pages**
Need to extract specific parts of a document? You can type in custom ranges (like `1-3, 5, 7-9`) or use the handy quick-preset range buttons. It flawlessly extracts just the pages you need and immediately updates your middle view so you can keep working on the extracted file.

**Crop Edges**
Perfect for removing scanning borders or awkward margins. Enter the exact margin values you want to trim from the top, bottom, left, or right. You can apply this crop to a single selected page or the entire document. The logic ensures your crop origin stays perfectly consistent every time.

**Rotate Pages**
Select a specific page (or all pages) and apply precise rotations: 90°, 180°, 270°, or 360°. You also have standard Left/Right rotation buttons. Unlike basic viewers, Vellum rotates the *actual page dimensions*, meaning your newly rotated pages are perfectly ready for footers or merging.

**Resize Pages**
Scale your page dimensions smoothly. You can stretch the width and height, or use the smart proportional resize feature. This allows you to match all pages to the exact width of a reference page, automatically scaling the heights so you don't get ugly white margins.

**Compress PDF**
Choose your engine: click "In-built" for standard Python compression, or "Ghostscript" for heavy lifting. Just type in your target file size (MB/KB). Vellum uses a smart iterative process that loops through DPI adjustments until it hits your target—guaranteeing it will *never* accidentally increase your file size.

**Adjust (Reorder & Delete)**
Need to do some quick cleanup? You can easily delete random individual pages from the document with a single click. You can also reorder pages smoothly without breaking the surrounding document structure.

**Add Footers**
Add page numbers with presets like "Page X of Y" or use Custom text. You get full control over font style, size (from micro to gigantic), alignment, and bottom-gap spacing. Best of all, it is *rotation-aware*—if you previously rotated a page, the footer will smartly place itself at the new bottom.

---

## 4. How to Use Vellum (Standard Workflow)

Vellum uses a strict **non-destructive workflow**. Your original files are *never* touched.

1. **Import:** Drag a PDF into the middle panel. It opens securely in a background temp folder.
2. **Select Pages:** Click pages in the middle panel, or use the **Select All / Selected** toggle on the right.
3. **Edit:** Pick a tool, adjust settings, and click **Make Changes**. The screen reloads instantly.
4. **Undo:** Made a mistake? Go to the right panel and hit the **Undo** button to revert.
5. **Export:** Review the auto-generated filename on the right panel, tweak your prefix/suffix if needed, and hit Export. 

---

## 5. Tips & Tricks

* **Instant Undo:** Because Vellum works entirely on temp files, jumping backward in your history is instant and completely safe.
* **Fast Deselect:** Double-clicking a selected page in the viewport instantly deselects it. multi-select works great with `Cmd/Ctrl` and `Shift`.
* **Cross-Platform:** Whether you are on your Mac Studio, a Windows laptop, or a Linux rig, the exact same commands and workflows apply. 

---

## 6. Bug Reports & Suggestions

Vellum is built to be a reliable everyday tool, but if you hit a snag or have an idea to make it better, I want to hear about it.

* **Found a Bug?** Open an Issue on the GitHub repository. Please include your OS, the tool you were using, and any error text printed in your terminal. 
* **Have a Suggestion?** Drop a feature request in the GitHub Issues tab. 

*Developed with care by Muzkkir.*
