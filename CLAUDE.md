# Mom Rescue Pack - Project Standards



## 1. Local Execution Policy (Elite Performance)

- **Problem:** The Claude Code sandbox has memory/CPU limits that cause 'Stream idle timeout' errors during heavy processing (e.g., ReportLab PDF generation).

- **Policy:** NEVER attempt to build production-grade PDFs or large batches inside the sandbox. 

- **Method:** Always write a standalone Python script (e.g., `build_skus.py`) for the Human to run locally.

- **Reasoning:** Local builds are superior because they utilize the full power of the host machine, ensuring zero timeouts and high-resolution output.



## 2. Professional PDF Standards

When generating scripts for PDFs (using ReportLab), you MUST:

- **Use Platypus:** Use the high-level layout engine to ensure professional document flow.

- **Vector Graphics:** All shapes and text must remain vector-based to ensure they stay razor-sharp and never blurry.

- **Commercial Margins:** Include a mandatory 0.25-inch 'safe zone' margin to prevent home printers from cutting off design elements.

- **Branding:** Automatically embed custom fonts and the 'Mom Rescue Pack' logo in every header.



## 3. Launch Workflow

For the 5 SKU launch, the generation script must:

1. **Build:** Generate all 5 high-end PDF SKUs.

2. **Package:** Include a 'Thank You & Instructions' cover page in the final bundle.

3. **Sync:** Push the final files to GitHub 'mom-rescue-assets'.

4. **Notion Link:** Update the 'Product Catalog' database in Notion with the GitHub Raw URLs.
