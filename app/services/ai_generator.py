"""
AI-powered website generation service using OpenAI
"""
from typing import Dict, Any, Optional
from openai import OpenAI
from app.core.config import settings
from app.core.settings_helper import get_api_key, get_active_prompt
import json


class AIWebsiteGenerator:
    """Service for generating website content using AI"""
    
    def __init__(self):
        self.client = None
        # Try to get API key from database first, fallback to env
        api_key = get_api_key('OPENAI_API_KEY') or settings.OPENAI_API_KEY
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    async def generate_website_content(
        self,
        business_data: Dict[str, Any],
        language: str = "hu"
    ) -> Dict[str, str]:
        """
        Generate complete website content using AI
        
        Args:
            business_data: Business information from Google Maps
            language: Target language for content
            
        Returns:
            Dictionary with HTML, CSS, and SEO content
        """
        if not self.client:
            return self._generate_fallback_content(business_data, language)
        
        try:
            # Generate content based on language
            prompt = self._build_generation_prompt(business_data, language)
            
            response = self.client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(language)},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
            
            content = response.choices[0].message.content
            return self._parse_generated_content(content, business_data)
            
        except Exception as e:
            print(f"Error generating website with AI: {e}")
            return self._generate_fallback_content(business_data, language)
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on language - check database first"""
        # Try to get from database
        db_prompt = get_active_prompt(language, "system")
        if db_prompt:
            return db_prompt
        
        # Fallback to hardcoded prompts
        prompts = {
            "hu": """Te egy szakértő weboldal-fejlesztő vagy, aki modern, reszponzív és SEO-optimalizált 
            weboldalakat készítesz kis- és középvállalkozások számára. Készíts professzionális, egyszerű 
            és hatékony weboldalakat HTML és CSS használatával.""",
            
            "en": """You are an expert web developer who creates modern, responsive, and SEO-optimized 
            websites for small and medium businesses. Create professional, simple, and effective websites 
            using HTML and CSS.""",
            
            "de": """Sie sind ein erfahrener Webentwickler, der moderne, responsive und SEO-optimierte 
            Websites für kleine und mittlere Unternehmen erstellt. Erstellen Sie professionelle, einfache 
            und effektive Websites mit HTML und CSS."""
        }
        
        return prompts.get(language, prompts["en"])
    
    def _build_generation_prompt(self, business_data: Dict[str, Any], language: str) -> str:
        """Build prompt for website generation - check database first"""
        business_name = business_data.get('name', 'Business')
        address = business_data.get('address', '')
        phone = business_data.get('phone', '')
        business_type = business_data.get('business_type', 'business')
        
        # Try to get custom prompt from database
        db_prompt = get_active_prompt(language, "generation")
        if db_prompt:
            # Replace variables in the prompt
            return db_prompt.format(
                business_name=business_name,
                address=address,
                phone=phone,
                business_type=business_type
            )
        
        # Fallback to hardcoded prompts
        prompts = {
            "hu": f"""Készíts egy egyszerű, modern weboldalat a következő vállalkozás számára:

Név: {business_name}
Cím: {address}
Telefon: {phone}
Típus: {business_type}

A weboldalnak tartalmaznia kell:
1. Fejléc a vállalkozás nevével és elérhetőségekkel
2. Bemutatkozó szekció
3. Szolgáltatások/termékek szekció
4. Kapcsolat szekció telefonszámmal és címmel
5. Interaktív elemek helye (contact form widget)

Válaszolj JSON formátumban: {{"html": "...", "css": "...", "seo_title": "...", "seo_description": "..."}}""",

            "en": f"""Create a simple, modern website for the following business:

Name: {business_name}
Address: {address}
Phone: {phone}
Type: {business_type}

The website should include:
1. Header with business name and contact info
2. About section
3. Services/products section
4. Contact section with phone and address
5. Interactive elements placeholder (contact form widget)

Reply in JSON format: {{"html": "...", "css": "...", "seo_title": "...", "seo_description": "..."}}"""
        }
        
        return prompts.get(language, prompts["en"])
    
    def _parse_generated_content(self, content: str, business_data: Dict[str, Any]) -> Dict[str, str]:
        """Parse AI-generated content"""
        try:
            # Try to parse as JSON
            data = json.loads(content)
            return {
                "html": data.get("html", ""),
                "css": data.get("css", ""),
                "seo_title": data.get("seo_title", business_data.get('name', '')),
                "seo_description": data.get("seo_description", "")
            }
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            # Fallback parsing if JSON parsing fails
            print(f"Failed to parse AI response as JSON: {e}")
            return self._generate_fallback_content(business_data, "hu")
    
    def _generate_fallback_content(self, business_data: Dict[str, Any], language: str) -> Dict[str, str]:
        """Generate fallback content when AI is not available"""
        business_name = business_data.get('name', 'Vállalkozás neve')
        address = business_data.get('address', '')
        phone = business_data.get('phone', '')
        
        html = f"""<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>{business_name}</h1>
        <p class="contact-info">📞 {phone} | 📍 {address}</p>
    </header>
    
    <main>
        <section class="hero">
            <h2>Üdvözöljük!</h2>
            <p>Professzionális szolgáltatások az Ön igényei szerint.</p>
        </section>
        
        <section class="services">
            <h2>Szolgáltatásaink</h2>
            <div class="service-grid">
                <div class="service-card">
                    <h3>Minőségi szolgáltatás</h3>
                    <p>Tapasztalt szakembereink várják.</p>
                </div>
            </div>
        </section>
        
        <section class="contact">
            <h2>Kapcsolat</h2>
            <p>📞 Telefon: {phone}</p>
            <p>📍 Cím: {address}</p>
            <div id="contact-widget"></div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 {business_name}. Minden jog fenntartva.</p>
    </footer>
</body>
</html>"""
        
        css = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    text-align: center;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.contact-info {
    font-size: 1.1rem;
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

section {
    margin: 3rem 0;
}

.hero {
    text-align: center;
    padding: 3rem 0;
}

.hero h2 {
    font-size: 2.5rem;
    color: #667eea;
    margin-bottom: 1rem;
}

.services {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 10px;
}

.service-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.service-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.contact {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
}

#contact-widget {
    margin-top: 2rem;
}

footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
}

@media (max-width: 768px) {
    header h1 {
        font-size: 1.8rem;
    }
    
    .hero h2 {
        font-size: 1.8rem;
    }
}"""
        
        return {
            "html": html,
            "css": css,
            "seo_title": business_name,
            "seo_description": f"{business_name} - {address}"
        }
