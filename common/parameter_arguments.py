import argparse
from argparse import Namespace

def parse_opt():
    parser = argparse.ArgumentParser(description='Image Yolo Dataset Generator for TASA Fase 2 Project.')
    parser.add_argument('--perfil_doc', dest='perfil_doc', action='store', 
                        default="docs/Perfil-Administrative-Assistant.pdf", 
                        help='PDF file, containing information about profile to search', required=True)
    parser.add_argument('--markdown', dest='markdown_extractor', action='store', 
                        default="pymupdf4llm", choices=['marker', 'megaparse', 'pymupdf4llm'],
                        help='Pdf markdown extractor', required=False)
    
    return parser
