"""
Example usage of the Google Map to Website API
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())
    print()

def generate_website(business_name, address, language="hu"):
    """Generate a website"""
    print(f"Generating website for: {business_name}")
    
    payload = {
        "business_name": business_name,
        "address": address,
        "language": language,
        "include_widgets": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/generator/generate",
        json=payload
    )
    
    if response.status_code == 200:
        website = response.json()
        print(f"✓ Website generated successfully!")
        print(f"  ID: {website['id']}")
        print(f"  Name: {website['business_name']}")
        print(f"  URL: {BASE_URL}{website['published_url']}")
        print()
        return website
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return None

def create_lead(website_id, name, email, phone, message):
    """Create a lead"""
    print(f"Creating lead: {name}")
    
    payload = {
        "website_id": website_id,
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "source": "contact_form"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/leads/",
        json=payload
    )
    
    if response.status_code == 200:
        lead = response.json()
        print(f"✓ Lead created successfully!")
        print(f"  ID: {lead['id']}")
        print(f"  Status: {lead['status']}")
        print()
        return lead
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return None

def add_widget(website_id, widget_type, name):
    """Add a widget to a website"""
    print(f"Adding widget: {name}")
    
    configurations = {
        "contact_form": {
            "fields": ["name", "email", "phone", "message"],
            "email_notification": True
        },
        "chatbot": {
            "greeting": "Szia! Miben segíthetek?",
            "ai_enabled": True
        },
        "map": {
            "show_directions": True,
            "show_street_view": True
        }
    }
    
    payload = {
        "website_id": website_id,
        "widget_type": widget_type,
        "name": name,
        "configuration": configurations.get(widget_type, {}),
        "position": "bottom",
        "is_active": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/widgets/",
        json=payload
    )
    
    if response.status_code == 200:
        widget = response.json()
        print(f"✓ Widget added successfully!")
        print(f"  ID: {widget['id']}")
        print(f"  Type: {widget['widget_type']}")
        print()
        return widget
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return None

def create_campaign(name, campaign_type, subject, content):
    """Create a marketing campaign"""
    print(f"Creating campaign: {name}")
    
    payload = {
        "name": name,
        "campaign_type": campaign_type,
        "subject": subject,
        "content": content,
        "target_criteria": {
            "status": "new"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/marketing/campaigns",
        json=payload
    )
    
    if response.status_code == 200:
        campaign = response.json()
        print(f"✓ Campaign created successfully!")
        print(f"  ID: {campaign['id']}")
        print(f"  Status: {campaign['status']}")
        print()
        return campaign
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return None

def get_analytics():
    """Get analytics overview"""
    print("Fetching analytics...")
    
    response = requests.get(f"{BASE_URL}/api/v1/marketing/analytics/overview")
    
    if response.status_code == 200:
        analytics = response.json()
        print("Analytics Overview:")
        print(f"  Total Leads: {analytics['leads']['total']}")
        print(f"  New Leads: {analytics['leads']['new']}")
        print(f"  Converted: {analytics['leads']['converted']}")
        print(f"  Conversion Rate: {analytics['leads']['conversion_rate']}%")
        print()
        return analytics
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def main():
    """Main example workflow"""
    print("=" * 60)
    print("Google Map to Website - API Examples")
    print("=" * 60)
    print()
    
    # Test health
    test_health()
    
    # Generate a website
    website = generate_website(
        business_name="Kovács Családi Étterem",
        address="Budapest, Andrássy út 1",
        language="hu"
    )
    
    if website:
        website_id = website['id']
        
        # Add widgets
        add_widget(website_id, "contact_form", "Kapcsolati Űrlap")
        add_widget(website_id, "chatbot", "AI Chatbot")
        add_widget(website_id, "map", "Térkép Widget")
        
        # Create leads
        create_lead(
            website_id,
            "Nagy János",
            "nagy.janos@example.com",
            "+36301234567",
            "Szeretnék asztalt foglalni 4 főre péntekre."
        )
        
        create_lead(
            website_id,
            "Kovács Mária",
            "kovacs.maria@example.com",
            "+36309876543",
            "Információt kérnék az étlapról."
        )
        
        # Create marketing campaign
        create_campaign(
            name="Üdvözlő Email Kampány",
            campaign_type="email",
            subject="Köszönjük az érdeklődését!",
            content="Tisztelt Ügyfelünk! Köszönjük, hogy felkereste weboldalunkat..."
        )
        
        # Get analytics
        get_analytics()
    
    print("=" * 60)
    print("Examples completed!")
    print(f"Visit {BASE_URL}/docs for interactive API documentation")
    print("=" * 60)

if __name__ == "__main__":
    main()
