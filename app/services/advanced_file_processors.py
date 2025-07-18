"""
Advanced File Processors for AI Recruitment Platform
Includes image processing, OCR, and enhanced PDF capabilities
"""

import logging
import io
from typing import Optional, Dict, Any, List
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from pymupdf import fitz
import PyPDF2
from docx import Document
import numpy as np
import cv2
from pathlib import Path

logger = logging.getLogger(__name__)

class AdvancedFileProcessor:
    """Advanced file processor with image processing, OCR, and enhanced capabilities"""
    
    def __init__(self):
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        self.supported_document_formats = ['.pdf', '.docx', '.doc', '.txt']
        
    async def process_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process any file type with advanced capabilities"""
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext in self.supported_image_formats:
                return await self._process_image(file_content, filename)
            elif file_ext in self.supported_document_formats:
                return await self._process_document(file_content, filename)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            raise
    
    async def _process_image(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process image files with OCR and enhancement"""
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(file_content))
            
            # Image preprocessing for better OCR
            processed_image = await self._preprocess_image(image)
            
            # Extract text using OCR
            text_content = await self._extract_text_from_image(processed_image)
            
            # Extract metadata
            metadata = await self._extract_image_metadata(image)
            
            return {
                "content": text_content,
                "metadata": metadata,
                "file_type": "image",
                "processing_method": "ocr",
                "confidence_score": metadata.get("ocr_confidence", 0.0)
            }
            
        except Exception as e:
            logger.error(f"Error processing image {filename}: {str(e)}")
            raise
    
    async def _process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process document files with enhanced capabilities"""
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext == '.pdf':
                return await self._process_pdf_advanced(file_content, filename)
            elif file_ext == '.docx':
                return await self._process_docx_advanced(file_content, filename)
            elif file_ext == '.txt':
                return await self._process_txt_advanced(file_content, filename)
            else:
                raise ValueError(f"Unsupported document type: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error processing document {filename}: {str(e)}")
            raise
    
    async def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale if needed
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.2)
            
            return image
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image
    
    async def _extract_text_from_image(self, image: Image.Image) -> str:
        """Extract text from image using OCR"""
        try:
            # Configure OCR for better accuracy
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@.-_() '
            
            # Extract text
            text = pytesseract.image_to_string(image, config=custom_config)
            
            # Get confidence scores
            data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
            confidence_scores = [int(score) for score in data['conf'] if int(score) > 0]
            
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            
            logger.info(f"OCR extracted {len(text)} characters with {avg_confidence:.2f}% confidence")
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            return ""
    
    async def _extract_image_metadata(self, image: Image.Image) -> Dict[str, Any]:
        """Extract metadata from image"""
        try:
            metadata = {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "width": image.width,
                "height": image.height,
                "dpi": image.info.get('dpi', None),
                "color_profile": image.info.get('icc_profile', None),
            }
            
            # Calculate OCR confidence
            try:
                data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                confidence_scores = [int(score) for score in data['conf'] if int(score) > 0]
                metadata["ocr_confidence"] = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            except:
                metadata["ocr_confidence"] = 0.0
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting image metadata: {str(e)}")
            return {}
    
    async def _process_pdf_advanced(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process PDF with advanced capabilities"""
        try:
            # Try PyMuPDF first (better for complex PDFs)
            try:
                doc = fitz.open(stream=file_content, filetype="pdf")
                text_content = ""
                metadata = {
                    "pages": len(doc),
                    "format": "PDF",
                    "processing_method": "pymupdf"
                }
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text_content += page.get_text() + "\n"
                    
                    # Extract images if present
                    image_list = page.get_images()
                    if image_list:
                        metadata["images_found"] = len(image_list)
                
                doc.close()
                
            except Exception as e:
                logger.warning(f"PyMuPDF failed, falling back to PyPDF2: {str(e)}")
                # Fallback to PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text_content = ""
                metadata = {
                    "pages": len(pdf_reader.pages),
                    "format": "PDF",
                    "processing_method": "pypdf2"
                }
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            
            return {
                "content": text_content,
                "metadata": metadata,
                "file_type": "pdf",
                "processing_method": metadata["processing_method"]
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {str(e)}")
            raise
    
    async def _process_docx_advanced(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process DOCX with advanced capabilities"""
        try:
            doc = Document(io.BytesIO(file_content))
            
            text_content = ""
            metadata = {
                "paragraphs": len(doc.paragraphs),
                "tables": len(doc.tables),
                "sections": len(doc.sections),
                "format": "DOCX",
                "processing_method": "python-docx"
            }
            
            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
            
            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text_content += cell.text + " "
                    text_content += "\n"
            
            return {
                "content": text_content,
                "metadata": metadata,
                "file_type": "docx",
                "processing_method": "python-docx"
            }
            
        except Exception as e:
            logger.error(f"Error processing DOCX {filename}: {str(e)}")
            raise
    
    async def _process_txt_advanced(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process TXT with advanced capabilities"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            text_content = ""
            
            for encoding in encodings:
                try:
                    text_content = file_content.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if not text_content:
                # Fallback to binary-safe decoding
                text_content = file_content.decode('latin-1')
            
            metadata = {
                "encoding": "detected",
                "size_bytes": len(file_content),
                "format": "TXT",
                "processing_method": "text_decode"
            }
            
            return {
                "content": text_content,
                "metadata": metadata,
                "file_type": "txt",
                "processing_method": "text_decode"
            }
            
        except Exception as e:
            logger.error(f"Error processing TXT {filename}: {str(e)}")
            raise
    
    async def extract_structured_data(self, text_content: str) -> Dict[str, Any]:
        """Extract structured data from text content"""
        try:
            # This would integrate with your AI parsing service
            # For now, return basic structure
            return {
                "text_length": len(text_content),
                "word_count": len(text_content.split()),
                "line_count": len(text_content.split('\n')),
                "has_email": '@' in text_content,
                "has_phone": any(char.isdigit() for char in text_content),
                "processing_timestamp": "2025-07-18T12:00:00Z"
            }
            
        except Exception as e:
            logger.error(f"Error extracting structured data: {str(e)}")
            return {}

# Global instance
advanced_file_processor = AdvancedFileProcessor() 