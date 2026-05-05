import os, shutil, subprocess
from io import BytesIO

import fitz
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


class PDFTools:
    def crop_pdf(self, input_path, output_path, left, right, top, bottom, page_indices=None):
        try:
            doc = fitz.open(input_path)
            for i, page in enumerate(doc):
                if page_indices is not None and i not in page_indices:
                    continue
                
                cb = page.cropbox
                mb = page.mediabox
                rot = page.rotation % 360
                
                if rot == 90:
                    dx0, dy0, dx1, dy1 = top, right, bottom, left
                elif rot == 180:
                    dx0, dy0, dx1, dy1 = right, bottom, left, top
                elif rot == 270:
                    dx0, dy0, dx1, dy1 = bottom, left, top, right
                else:
                    dx0, dy0, dx1, dy1 = left, top, right, bottom

                new_rect = fitz.Rect(cb.x0 + dx0, cb.y0 + dy0, cb.x1 - dx1, cb.y1 - dy1) & mb

                if new_rect.is_empty or new_rect.is_infinite or new_rect.width < 10 or new_rect.height < 10:
                    print(f"WARNING: Crop on page {i} invalid or too small — skipped.")
                    continue

                page.set_cropbox(new_rect)
                
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
        except Exception as ex:
            raise RuntimeError(f"Crop failed: {ex}") from ex


    # ══════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════

    def add_footer(self, input_path, output_path,
               text_template="Page {n} of {total}",
               alignment="right",
               font_name="Helvetica",
               font_size=10,
               gap_cm=0.0,
               page_indices=None,
               filename="",
               page_rotations=None):
        if page_rotations is None:
            page_rotations = {}
        try:
            src      = fitz.open(input_path)
            total    = len(src)
            out      = fitz.open()
            gap_pts  = gap_cm * 28.3465
            footer_h = 30.0

            for i in range(total):
                try:
                    src_page = src[i]
                    rot      = page_rotations.get(i, src_page.rotation) % 360
                    raw_w    = float(src_page.rect.width)
                    raw_h    = float(src_page.rect.height)

                    if rot in (90, 270):
                        render_w, render_h = raw_h, raw_w
                    else:
                        render_w, render_h = raw_w, raw_h

                    extra    = gap_pts + footer_h
                    new_w    = raw_w
                    new_h    = raw_h + (extra if rot in (0, 180) else 0)
                    new_w    = raw_w + (extra if rot in (90, 270) else 0)

                    new_page = out.new_page(width=new_w, height=new_h)

                    if rot in (0, 180):
                        content_rect = fitz.Rect(0, 0, raw_w, raw_h)
                    elif rot == 90:
                        content_rect = fitz.Rect(0, 0, raw_w, raw_h)
                    else:
                        content_rect = fitz.Rect(0, 0, raw_w, raw_h)

                    new_page.show_pdf_page(content_rect, src, i)

                    if page_indices is not None and i not in page_indices:
                        continue

                    text = (text_template
                            .replace("{n}",        str(i + 1))
                            .replace("{total}",    str(total))
                            .replace("{filename}", filename))

                    overlay_bytes = self._make_footer_bytes(
                        rot, render_w, render_h, new_w, new_h,
                        raw_w, raw_h, gap_pts, footer_h,
                        text, alignment, font_name, font_size)

                    overlay_doc = fitz.open("pdf", overlay_bytes)
                    new_page.show_pdf_page(new_page.rect, overlay_doc, 0, overlay=True)
                    overlay_doc.close()

                except Exception as ex:
                    print(f"WARNING: Footer on page {i} failed: {ex}")

            out.save(output_path, garbage=4, deflate=True)
            out.close()
            src.close()
        except Exception as ex:
            raise RuntimeError(f"Add footer failed: {ex}") from ex

    def _make_footer_bytes(self, rot, render_w, render_h,
                            new_w, new_h, raw_w, raw_h,
                            gap_pts, footer_h,
                            text, alignment, font_name, font_size):
        try:
            packet = BytesIO()
            c      = canvas.Canvas(packet, pagesize=(new_w, new_h))
            margin = 40
            # In ReportLab y=0 is bottom. Footer sits at bottom of expanded page.
            # For rot==0: content occupies top portion, footer in bottom `footer_h` strip.
            # ReportLab origin is bottom-left, so footer y coords are near 0.
            y_text = footer_h - 18
            y_line = footer_h - 4

            c.saveState()

            if rot == 0 or rot == 180:
                draw_w = render_w
            else:
                draw_w = render_h

            c.setFont(font_name, font_size)
            c.setFillColorRGB(0.2, 0.2, 0.2)
            if alignment == "left":
                c.drawString(margin, y_text, text)
            elif alignment == "center":
                c.drawCentredString(draw_w / 2.0, y_text, text)
            else:
                c.drawRightString(draw_w - margin, y_text, text)

            c.setLineWidth(0.5)
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.line(margin, y_line, draw_w - margin, y_line)

            c.restoreState()
            c.save()
            return packet.getvalue()
        except Exception as ex:
            raise RuntimeError(f"Make footer bytes failed: {ex}") from ex


    # ══════════════════════════════════════════
    # MERGE
    # ══════════════════════════════════════════
    def merge_pdfs(self, input_paths, output_path):
        try:
            writer = PdfWriter()
            for p in input_paths:
                try:
                    reader = PdfReader(p)
                    for page in reader.pages:
                        writer.add_page(page)
                except Exception as ex:
                    print(f"WARNING: Skipping {p}: {ex}")
            if len(writer.pages) == 0:
                raise ValueError("No pages were merged — check input files.")
            with open(output_path, "wb") as f:
                writer.write(f)
        except Exception as ex:
            raise RuntimeError(f"Merge failed: {ex}") from ex

    # ══════════════════════════════════════════
    # SPLIT
    # ══════════════════════════════════════════
    def split_indices(self, input_path, output_path, indices):
        """Extract specific 0-based page indices into one output file."""
        try:
            reader = PdfReader(input_path)
            total  = len(reader.pages)
            writer = PdfWriter()
            for i in indices:
                if 0 <= i < total:
                    writer.add_page(reader.pages[i])
            if len(writer.pages) == 0:
                raise ValueError("No valid pages found in the given range.")
            with open(output_path, "wb") as f:
                writer.write(f)
        except Exception as ex:
            raise RuntimeError(f"Split indices failed: {ex}") from ex

    def split_ranges_separately(self, input_path, output_dir, range_text):
        """Parse range_text like '1-3, 5, 7-9' and produce one PDF per group."""
        try:
            reader    = PdfReader(input_path)
            total     = len(reader.pages)
            base      = os.path.splitext(os.path.basename(input_path))[0]
            parts     = [p.strip() for p in range_text.split(",") if p.strip()]
            out_paths = []
            for part in parts:
                try:
                    indices = self._parse_single_range(part, total)
                    if not indices:
                        continue
                    writer = PdfWriter()
                    for i in indices:
                        writer.add_page(reader.pages[i])
                    label = part.replace("-", "_").replace(" ", "")
                    out   = self._unique_path(
                        os.path.join(output_dir, f"{base}_split_{label}.pdf"))
                    with open(out, "wb") as f:
                        writer.write(f)
                    out_paths.append(out)
                except Exception as ex:
                    print(f"WARNING: Skipping range '{part}': {ex}")
            return out_paths
        except Exception as ex:
            raise RuntimeError(f"Split ranges failed: {ex}") from ex

    def split_every_page(self, input_path, output_dir):
        """Split every page into its own PDF file."""
        try:
            reader    = PdfReader(input_path)
            base      = os.path.splitext(os.path.basename(input_path))[0]
            out_paths = []
            for i, page in enumerate(reader.pages):
                try:
                    writer = PdfWriter()
                    writer.add_page(page)
                    out = self._unique_path(
                        os.path.join(output_dir, f"{base}_page_{i+1:03d}.pdf"))
                    with open(out, "wb") as f:
                        writer.write(f)
                    out_paths.append(out)
                except Exception as ex:
                    print(f"WARNING: Could not split page {i}: {ex}")
            return out_paths
        except Exception as ex:
            raise RuntimeError(f"Split every page failed: {ex}") from ex

    def _parse_single_range(self, part, total):
        try:
            part = part.strip()
            if "-" in part:
                a, b = part.split("-", 1)
                a = max(0, int(a.strip()) - 1)
                b = min(total - 1, int(b.strip()) - 1)
                return list(range(a, b + 1)) if a <= b else []
            else:
                i = int(part) - 1
                return [i] if 0 <= i < total else []
        except Exception:
            return []

    def _unique_path(self, path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        i = 1
        while os.path.exists(f"{base}_{i}{ext}"):
            i += 1
        return f"{base}_{i}{ext}"

    # ══════════════════════════════════════════
    # ROTATE
    # ══════════════════════════════════════════

    def rotate_pages(self, input_path, output_path, angle, page_indices=None):
        """
        Bakes rotation into page content via show_pdf_page.
        Output pages always have /Rotate=0 so all downstream tools work correctly.
        """
        try:
            src     = fitz.open(input_path)
            out_doc = fitz.open()
            angle   = angle % 360

            for i in range(len(src)):
                try:
                    page = src[i]
                    if page_indices is not None and i not in page_indices:
                        out_doc.insert_pdf(src, from_page=i, to_page=i)
                        continue
                    if angle == 0:
                        out_doc.insert_pdf(src, from_page=i, to_page=i)
                        continue

                    # page.bound() returns the VISUAL rectangle — it already
                    # accounts for any existing /Rotate flag on the source page.
                    vis   = page.bound()
                    vis_w = vis.width
                    vis_h = vis.height

                    # New page dimensions after the additional rotation
                    if angle in (90, 270):
                        new_w, new_h = vis_h, vis_w
                    else:
                        new_w, new_h = vis_w, vis_h

                    new_page = out_doc.new_page(width=new_w, height=new_h)
                    # show_pdf_page renders the visual content (honouring source /Rotate)
                    # then adds the requested angle on top — result is fully baked in.
                    new_page.show_pdf_page(
                        fitz.Rect(0, 0, new_w, new_h),
                        src, i,
                        rotate=angle
                    )
                except Exception as ex:
                    print(f"WARNING: Could not rotate page {i}: {ex}")
                    try:
                        out_doc.insert_pdf(src, from_page=i, to_page=i)
                    except Exception:
                        pass

            src.close()
            out_doc.save(output_path, garbage=4, deflate=True)
            out_doc.close()
        except Exception as ex:
            raise RuntimeError(f"Rotate failed: {ex}") from ex

    # ══════════════════════════════════════════
    # RESIZE
    # ══════════════════════════════════════════
    def resize_to_ref_width(self, input_path, output_path,
                             ref_page_idx=0, page_indices=None):
        try:
            src = fitz.open(input_path)
            if ref_page_idx >= len(src):
                ref_page_idx = 0
            ref = src[ref_page_idx]
            # Use visual width (accounting for rotation)
            if ref.rotation in (90, 270):
                target_w = float(ref.rect.height)
            else:
                target_w = float(ref.rect.width)

            out_doc = fitz.open()
            for i in range(len(src)):
                try:
                    page = src[i]
                    if page_indices is not None and i not in page_indices:
                        out_doc.insert_pdf(src, from_page=i, to_page=i)
                        continue
                    if page.rotation in (90, 270):
                        sw = float(page.rect.height)
                        sh = float(page.rect.width)
                    else:
                        sw = float(page.rect.width)
                        sh = float(page.rect.height)
                    if sw == 0:
                        out_doc.insert_pdf(src, from_page=i, to_page=i)
                        continue
                    scale    = target_w / sw
                    new_w    = target_w
                    new_h    = sh * scale
                    new_page = out_doc.new_page(width=new_w, height=new_h)
                    new_page.show_pdf_page(
                        fitz.Rect(0, 0, new_w, new_h), src, i)
                except Exception as ex:
                    print(f"WARNING: Could not resize page {i}: {ex}")
                    try:
                        out_doc.insert_pdf(src, from_page=i, to_page=i)
                    except Exception:
                        pass

            src.close()
            out_doc.save(output_path, garbage=4, deflate=True)
            out_doc.close()
        except Exception as ex:
            raise RuntimeError(f"Resize failed: {ex}") from ex

    # ══════════════════════════════════════════
    # COMPRESS — Built-in (fitz rasterise)
    # ══════════════════════════════════════════
    def compress_pdf_builtin(self, input_path, output_path, target_mb,
                              progress_cb=None):
        """
        Compress by rasterising pages at decreasing zoom levels.
        Uses fitz pixmap directly — no intermediate PNG encoding.
        """
        try:
            target_bytes   = target_mb * 1024 * 1024
            original_bytes = os.path.getsize(input_path)

            if original_bytes <= target_bytes:
                shutil.copy2(input_path, output_path)
                if progress_cb:
                    progress_cb(100,
                        f"Already under target: "
                        f"{original_bytes/(1024*1024):.2f} MB")
                return output_path, original_bytes / (1024 * 1024)

            # Zoom levels to try (lower = smaller file, worse quality)
            zoom_steps = [1.5, 1.2, 1.0, 0.85, 0.7, 0.55, 0.4, 0.3]
            best_path  = None
            best_size  = original_bytes

            for idx, zoom in enumerate(zoom_steps):
                if progress_cb:
                    pct = int((idx + 1) / len(zoom_steps) * 90)
                    progress_cb(pct, f"Trying zoom = {zoom:.2f}…")

                tmp = output_path + f"_z{idx}.pdf"
                try:
                    src     = fitz.open(input_path)
                    out_doc = fitz.open()
                    mat     = fitz.Matrix(zoom, zoom)

                    for page_num in range(len(src)):
                        try:
                            page     = src[page_num]
                            pix      = page.get_pixmap(matrix=mat, alpha=False)
                            # New page with ORIGINAL dimensions so content fits
                            new_page = out_doc.new_page(
                                width=page.rect.width,
                                height=page.rect.height)
                            new_page.insert_image(
                                fitz.Rect(0, 0, page.rect.width, page.rect.height),
                                pixmap=pix)
                        except Exception as ex:
                            print(f"WARNING: Page {page_num} at zoom={zoom}: {ex}")

                    out_doc.save(tmp, deflate=True, garbage=4)
                    out_doc.close()
                    src.close()

                    sz = os.path.getsize(tmp)
                    if sz < best_size:
                        if best_path and os.path.exists(best_path):
                            try:
                                os.remove(best_path)
                            except Exception:
                                pass
                        best_path = tmp
                        best_size = sz
                    else:
                        try:
                            os.remove(tmp)
                        except Exception:
                            pass

                    if best_size <= target_bytes:
                        break

                except Exception as ex:
                    print(f"ERROR: Compression at zoom={zoom}: {ex}")
                    if os.path.exists(tmp):
                        try:
                            os.remove(tmp)
                        except Exception:
                            pass
                    continue

            if best_path and os.path.exists(best_path):
                shutil.move(best_path, output_path)
            else:
                shutil.copy2(input_path, output_path)
                best_size = original_bytes

            if progress_cb:
                progress_cb(100, f"Final: {best_size/(1024*1024):.2f} MB")

            return output_path, best_size / (1024 * 1024)

        except Exception as ex:
            raise RuntimeError(f"Built-in compression failed: {ex}") from ex

    # ══════════════════════════════════════════
    # COMPRESS — Ghostscript
    # ══════════════════════════════════════════
    def compress_pdf(self, input_path, output_path, target_mb, progress_cb=None):
        try:
            target_bytes   = target_mb * 1024 * 1024
            original_bytes = os.path.getsize(input_path)

            if original_bytes <= target_bytes:
                shutil.copy2(input_path, output_path)
                if progress_cb:
                    progress_cb(100,
                        f"Already under target: "
                        f"{original_bytes/(1024*1024):.2f} MB")
                return output_path, original_bytes / (1024 * 1024)

            gs = self._find_ghostscript()
            if not gs:
                raise RuntimeError(
                    "Ghostscript not found.\n"
                    "Install with:  brew install ghostscript  "
                    "or  sudo apt install ghostscript")

            dpi_steps = [150, 120, 96, 72, 60, 48, 36]
            best_path = None
            best_size = original_bytes

            for idx, dpi in enumerate(dpi_steps):
                if progress_cb:
                    pct = int((idx + 1) / len(dpi_steps) * 90)
                    progress_cb(pct, f"Trying DPI = {dpi}…")

                tmp = output_path + f"_dpi{dpi}.pdf"
                try:
                    self._run_gs(gs, input_path, tmp, dpi)
                    sz = os.path.getsize(tmp)
                    if sz < best_size:
                        if best_path and os.path.exists(best_path):
                            try:
                                os.remove(best_path)
                            except Exception:
                                pass
                        best_path = tmp
                        best_size = sz
                    else:
                        try:
                            os.remove(tmp)
                        except Exception:
                            pass
                    if best_size <= target_bytes:
                        break
                except Exception as ex:
                    print(f"WARNING: GS DPI={dpi} failed: {ex}")
                    if os.path.exists(tmp):
                        try:
                            os.remove(tmp)
                        except Exception:
                            pass
                    continue

            if best_path and os.path.exists(best_path):
                shutil.move(best_path, output_path)
            else:
                shutil.copy2(input_path, output_path)
                best_size = original_bytes

            if progress_cb:
                progress_cb(100, f"Final: {best_size/(1024*1024):.2f} MB")

            return output_path, best_size / (1024 * 1024)

        except Exception as ex:
            raise RuntimeError(f"Ghostscript compression failed: {ex}") from ex

    def _run_gs(self, gs_path, input_path, output_path, dpi):
        try:
            cmd = [
                gs_path,
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.4",
                "-dPDFSETTINGS=/screen",
                "-dNOPAUSE", "-dQUIET", "-dBATCH",
                f"-r{dpi}",
                f"-dColorImageResolution={dpi}",
                f"-dGrayImageResolution={dpi}",
                f"-dMonoImageResolution={dpi}",
                f"-sOutputFile={output_path}",
                input_path,
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr.decode(errors="replace")[:400])
        except subprocess.TimeoutExpired:
            raise RuntimeError("Ghostscript timed out after 120 seconds.")
        except Exception as ex:
            raise RuntimeError(f"Ghostscript error: {ex}") from ex

    def _find_ghostscript(self):
        for name in ("gs", "gswin64c", "gswin32c"):
            try:
                r = subprocess.run(
                    ["which", name], capture_output=True, timeout=5)
                if r.returncode == 0:
                    p = r.stdout.decode().strip()
                    if p:
                        return p
            except Exception:
                pass
        for path in ("/opt/homebrew/bin/gs",
                     "/usr/local/bin/gs",
                     "/usr/bin/gs"):
            if os.path.exists(path):
                return path
        return None

    # ══════════════════════════════════════════
    # DELETE PAGES
    # ══════════════════════════════════════════
    def delete_pages(self, input_path, output_path, page_indices):
        try:
            doc    = fitz.open(input_path)
            total  = len(doc)
            to_del = sorted(
                [i for i in page_indices if 0 <= i < total],
                reverse=True)
            if not to_del:
                raise ValueError("No valid page indices to delete.")
            for idx in to_del:
                try:
                    doc.delete_page(idx)
                except Exception as ex:
                    print(f"WARNING: Could not delete page {idx}: {ex}")
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
        except Exception as ex:
            raise RuntimeError(f"Delete pages failed: {ex}") from ex

    # =====================
    # ReOrder Pages
    # =====================
    def reorder_pages(self, input_path, output_path, new_order):
        src = fitz.open(input_path)
        out = fitz.open()
        for i in new_order:
            out.insert_pdf(src, from_page=i, to_page=i)
        out.save(output_path, garbage=4, deflate=True)
        out.close()
        src.close()


    # ══════════════════════════════════════════
    # DECRYPT
    # ══════════════════════════════════════════
    def decrypt_pdf(self, input_path, output_path, password):
        try:
            doc = fitz.open(input_path)
            if not doc.needs_pass:
                doc.close()
                shutil.copy2(input_path, output_path)
                return True, "File was not encrypted — copied as-is."
            if not doc.authenticate(password):
                doc.close()
                return False, "Incorrect password."
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            return True, "Decrypted successfully."
        except Exception as ex:
            return False, f"Decrypt error: {ex}"