"""
Railway-Optimized File Processors for AI Recruitment Platform
Lightweight version without heavy dependencies
"""

import logging
import io
from typing import Optional, Dict, Any, List
from PIL import Image, ImageEnhance, ImageFilter
import PyPDF2
from docx import Document
from pathlib import Path
import base64

logger = logging.getLogger(__name__)

class RailwayFileProcessor:
    """Railway-optimized file processor with lightweight capabilities"""
    
    def __init__(self):
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.bmp']
        self.supported_document_formats = ['.pdf', '.docx', '.txt']
        
    async def process_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process any file type with Railway-optimized capabilities"""
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext in self.supported_image_formats:
                return await self._process_image_lightweight(file_content, filename)
            elif file_ext in self.supported_document_formats:
                return await self._process_document_lightweight(file_content, filename)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            raise
    
    async def _process_image_lightweight(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process image files with lightweight capabilities"""
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(file_content))
            
            # Basic image preprocessing
            processed_image = await self._preprocess_image_lightweight(image)
            
            # For Railway, we'll return image metadata instead of OCR
            # OCR can be added later if needed
            metadata = await self._extract_image_metadata_lightweight(image)
            
            return {
                "content": f"Image file: {filename} - OCR not available in Railway mode",
                "metadata": metadata,
                "file_type": "image",
                "processing_method": "lightweight",
                "confidence_score": 0.8  # High confidence for image processing
            }
            
        except Exception as e:
            logger.error(f"Error processing image {filename}: {str(e)}")
            raise
    
    async def _process_document_lightweight(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process document files with lightweight capabilities"""
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext == '.pdf':
                return await self._process_pdf_lightweight(file_content, filename)
            elif file_ext == '.docx':
                return await self._process_docx_lightweight(file_content, filename)
            elif file_ext == '.txt':
                return await self._process_txt_lightweight(file_content, filename)
            else:
                raise ValueError(f"Unsupported document type: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error processing document {filename}: {str(e)}")
            raise
    
    async def _preprocess_image_lightweight(self, image: Image.Image) -> Image.Image:
        """Lightweight image preprocessing"""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Basic enhancement
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            return image
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image
    
    async def _extract_image_metadata_lightweight(self, image: Image.Image) -> Dict[str, Any]:
        """Extract metadata from image"""
        try:
            metadata = {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "width": image.width,
                "height": image.height,
                "dpi": image.info.get('dpi', None),
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting image metadata: {str(e)}")
            return {}
    
    async def _process_pdf_lightweight(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process PDF with lightweight capabilities"""
        try:
            # Use PyPDF2 for Railway compatibility
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
                "processing_method": "pypdf2"
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {str(e)}")
            raise
    
    async def _process_docx_lightweight(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process DOCX with lightweight capabilities"""
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
    
    async def _process_txt_lightweight(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process TXT with lightweight capabilities"""
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
railway_file_processor = RailwayFileProcessor() 