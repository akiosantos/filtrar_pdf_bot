import re
from pypdf import PdfReader, PdfWriter

PDF_ENTRADA = "enel_completo.pdf"
PDF_SAIDA = "enel_filtrado.pdf"

def tem_valor_monetario(texto):
    if not texto:
        return False
    return bool(re.search(r"r\$\s*\d+[.,]\d{2}", texto.lower()))

def pagina_interessa(texto):
    if not texto:
        return False

    t = texto.lower()

    tem_instalacao = "instala" in t or "uc" in t
    tem_vencimento = "vencimento" in t
    tem_valor = tem_valor_monetario(t)

    criterios = sum([tem_instalacao, tem_vencimento, tem_valor])

    return criterios >= 2


def filtrar_pdf():
    reader = PdfReader(PDF_ENTRADA)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        texto = page.extract_text()

        if pagina_interessa(texto):
            print(f"✅ Página {i+1} mantida")
            writer.add_page(page)
        else:
            print(f"❌ Página {i+1} descartada")

    with open(PDF_SAIDA, "wb") as f:
        writer.write(f)

    print("\nArquivo gerado:", PDF_SAIDA)


if __name__ == "__main__":
    filtrar_pdf()
