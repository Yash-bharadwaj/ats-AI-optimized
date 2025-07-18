"""
Railway-Optimized File Processors for AI Recruitment Platform
Simplified version without heavy dependencies
"""

import logging
import io
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class RailwayFileProcessor:
    """Railway-optimized file processor with basic capabilities"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.jpg', '.jpeg', '.png']
        
    async def process_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process any file type with Railway-optimized capabilities"""
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext in self.supported_formats:
                return await self._process_file_basic(file_content, filename)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            raise
    
    async def _process_file_basic(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process file with basic capabilities"""
        try:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext == '.pdf':
                return await self._process_pdf_basic(file_content, filename)
            elif file_ext == '.docx':
                return await self._process_docx_basic(file_content, filename)
            elif file_ext == '.txt':
                return await self._process_txt_basic(file_content, filename)
            elif file_ext in ['.jpg', '.jpeg', '.png']:
                return await self._process_image_basic(file_content, filename)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            raise
    
    async def _process_pdf_basic(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process PDF with basic capabilities"""
        try:
            # Try to use PyPDF2
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text_content = ""
                metadata = {
                    "pages": len(pdf_reader.pages),
                    "format": "PDF",
                    "processing_method": "pypdf2"
                }
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
                    
            except ImportError:
                logger.warning("PyPDF2 not available, using basic text extraction")
                text_content = file_content.decode('latin-1')
                metadata = {
                    "format": "PDF",
                    "processing_method": "basic_decode"
                }
            
            return {
                "content": text_content,
                "metadata": metadata,
                "file_type": "pdf",
                "processing_method": metadata["processing_method"]
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {str(e)}")
            raise
    
    async def _process_docx_basic(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process DOCX with basic capabilities"""
        try:
            # Try to use python-docx
            try:
                from docx import Document
                doc = Document(io.BytesIO(file_content))
                
                text_content = ""
                metadata = {
                    "paragraphs": len(doc.paragraphs),
                    "tables": len(doc.tables),
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
                        
            except ImportError:
                logger.warning("python-docx not available, using basic text extraction")
                text_content = file_content.decode('latin-1')
                metadata = {
                    "format": "DOCX",
                    "processing_method": "basic_decode"
                }
            
            return {
                "content": text_content,
                "metadata": metadata,
                "file_type": "docx",
                "processing_method": metadata["processing_method"]
            }
            
        except Exception as e:
            logger.error(f"Error processing DOCX {filename}: {str(e)}")
            raise
    
    async def _process_txt_basic(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process TXT with basic capabilities"""
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
    
    async def _process_image_basic(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process image files with basic capabilities"""
        try:
            # Try to use PIL for basic image processing
            try:
                from PIL import Image
                image = Image.open(io.BytesIO(file_content))
                
                metadata = {
                    "format": image.format,
                    "mode": image.mode,
                    "size": image.size,
                    "width": image.width,
                    "height": image.height,
                    "processing_method": "pil"
                }
                
            except ImportError:
                logger.warning("PIL not available, using basic image processing")
                metadata = {
                    "format": "unknown",
                    "size_bytes": len(file_content),
                    "processing_method": "basic"
                }
            
            return {
                "content": f"Image file: {filename} - Text extraction not available in Railway mode",
                "metadata": metadata,
                "file_type": "image",
                "processing_method": metadata["processing_method"],
                "confidence_score": 0.8
            }
            
        except Exception as e:
            logger.error(f"Error processing image {filename}: {str(e)}")
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