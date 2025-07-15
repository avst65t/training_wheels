import subprocess
import os

def convert_tex_to_pdf(tex_file):
    if not os.path.exists(tex_file):
        raise FileNotFoundError(f"The file '{tex_file}' does not exist.")
    
    tex_dir = os.path.dirname(os.path.abspath(tex_file))
    tex_filename = os.path.basename(tex_file)

    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_filename],
            cwd=tex_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        print("LaTeX compilation output:")
        print(result.stdout)

        pdf_file = tex_filename.replace(".tex", ".pdf")

        if os.path.exists(os.path.join(tex_dir, pdf_file)):
            print(f"PDF generated successfully: {pdf_file}")
        else:
            print("PDF generation failed. Check the .log file for errors.")

    except subprocess.CalledProcessError as e:
        print("Error during LaTeX compilation:")
        print(e.stderr)  # This will print the full error log
        print("Check the generated .log file in the same directory for details.")

# Example usage
convert_tex_to_pdf("ai_report_v2.tex")
