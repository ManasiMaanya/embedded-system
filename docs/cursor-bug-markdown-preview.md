# Cursor bug report (paste this)

**Status:** Ready to submit. This agent cannot log into forum.cursor.com as you. Paste the block below into:

1. Cursor: **Help → Report Issue** (or the in-app feedback form), and/or
2. New topic: [https://forum.cursor.com/c/bug-reports/6](https://forum.cursor.com/c/bug-reports/6)

Related threads (same renderer): [166003](https://forum.cursor.com/t/markdown-in-editor-preview-shows-blank-black-pane/166003), [163908](https://forum.cursor.com/t/markdown-preview-fails-to-load/163908), [164460](https://forum.cursor.com/t/makrdown-preview-is-broken/164460). This report adds: **3.17.21**, **Windows**, **classic `markdown.showPreviewToSide` also does nothing** when `editorLangId == markdown` is false, MPE activates but never shows a webview.

---

## Title

Cursor 3.17.21 (Windows): in-tab Markdown Preview blank; `markdown.showPreviewToSide` / MPE never open a webview (`editorLangId` not `markdown`)

## Environment

- Cursor **3.17.21** stable (`commit` `8f2a112cb2845a97b75fd932ea5c470579ca4060`, `date` 2026-08-25)
- `vscodeVersion` in product.json: **1.128.0**
- OS: **Windows_NT 10.0.26200** (Win11)
- Built-in `markdown-language-features` is present (`markdown.showPreview` / `markdown.showPreviewToSide` exist in the extension `package.json`)
- Extensions installed: `shd101wyy.markdown-preview-enhanced` 0.8.30 (exthost: **activated success** on `onStartupFinished` and `onLanguage:markdown`), `bierner.markdown-mermaid` 1.32.1
- Same `.md` files **render correctly in a browser** (KaTeX + GFM)

## What happens

1. Open a normal `.md` file (example: project `docs/overview.md` or `docs/architecture.md`: headings, GFM tables, fenced ASCII diagrams, `$...$` / `$$...$$` math).
2. Use the editor **Preview** pill (Cursor rich markdown editor, not VS Code side preview).
3. **Result:** blank / empty preview. No error toast. Status bar 0 errors.
4. Command Palette **Markdown: Open Preview to the Side** and **Markdown Preview Enhanced: Open Preview to the Side**: **no preview webview appears**.
5. `Ctrl+Shift+V` bound to `markdown.showPreviewToSide` with `when: editorLangId == markdown`: **does nothing** (context likely false). Binding the same command with `when: resourceExtname == '.md'` still no visible webview in this session.
6. Workaround that **does** work: generate HTML and open in the system browser. In-IDE preview does not.

## Exthost (MPE is not crashing)

```
ExtensionService#_doActivateExtension shd101wyy.markdown-preview-enhanced
Extension activated success: shd101wyy.markdown-preview-enhanced — ~850ms
```

No MPE webview error in `exthost.log`. Failure looks like **UI never hosts the preview**, not an extension throw.

## Expected

- In-tab Preview shows rendered Markdown (or a visible error, not a black/empty pane).
- `markdown.showPreviewToSide` opens the classic VS Code markdown webview.
- `editorLangId == markdown` is true for `.md` in both the rich editor and the default text editor so keybindings and MPE `when` clauses fire.

## Settings tried (did not restore in-IDE preview)

```json
"workbench.editorAssociations": { "*.md": "default" },
"files.associations": { "*.md": "markdown" },
"markdown.math.enabled": true,
"markdown-preview-enhanced.previewMode": "Multiple Previews"
```

Unbound `markdownEditor.toggleMode` from `ctrl+shift+v`.

## Why this is worse than the known “blank Preview pill” bugs

Staff already track the rich Preview renderer going blank on some CommonMark shapes (`listItem` content check / `RangeError: Invalid content for node listItem`). On **3.17.21 Windows**, the **classic** `markdown.showPreviewToSide` path also fails to show a panel, so the documented workaround (“use Markdown: Open Preview”) is not available.

## Does this stop you using Cursor?

No — editing works; in-IDE Markdown preview does not.
