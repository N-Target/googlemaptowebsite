// Admin Panel JavaScript

const API_BASE = '/api/v1';
const ADMIN_API = '/api/v1/admin';

// Navigation
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    
    // Show selected section
    document.getElementById(`${sectionName}-section`).classList.remove('hidden');
    
    // Update active link
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.closest('.sidebar-link').classList.add('active');
    
    // Load section data
    loadSectionData(sectionName);
}

function loadSectionData(sectionName) {
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'settings':
            loadSettings();
            break;
        case 'prompts':
            loadPrompts();
            break;
        case 'websites':
            loadWebsites();
            break;
        case 'leads':
            loadLeads();
            break;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${ADMIN_API}/dashboard/stats`);
        const data = await response.json();
        
        // Update stats
        document.getElementById('stat-websites').textContent = data.stats.total_websites;
        document.getElementById('stat-leads').textContent = data.stats.total_leads;
        document.getElementById('stat-widgets').textContent = data.stats.total_widgets;
        document.getElementById('stat-campaigns').textContent = data.stats.total_campaigns;
        
        // Update recent websites
        const recentWebsitesEl = document.getElementById('recent-websites');
        if (data.recent_websites.length > 0) {
            recentWebsitesEl.innerHTML = data.recent_websites.map(w => `
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                        <p class="font-semibold">${w.business_name}</p>
                        <p class="text-sm text-gray-500">${w.language.toUpperCase()} - ${w.status}</p>
                    </div>
                    <span class="text-xs text-gray-400">${new Date(w.created_at).toLocaleDateString('hu')}</span>
                </div>
            `).join('');
        } else {
            recentWebsitesEl.innerHTML = '<p class="text-gray-500">Még nincs generált weboldal</p>';
        }
        
        // Update recent leads
        const recentLeadsEl = document.getElementById('recent-leads');
        if (data.recent_leads.length > 0) {
            recentLeadsEl.innerHTML = data.recent_leads.map(l => `
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                        <p class="font-semibold">${l.name}</p>
                        <p class="text-sm text-gray-500">${l.email}</p>
                    </div>
                    <span class="px-2 py-1 text-xs rounded-full ${l.status === 'new' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}">${l.status}</span>
                </div>
            `).join('');
        } else {
            recentLeadsEl.innerHTML = '<p class="text-gray-500">Még nincs lead</p>';
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Settings
async function loadSettings() {
    try {
        const response = await fetch(`${ADMIN_API}/settings`);
        const settings = await response.json();
        
        // Load API keys if they exist
        settings.forEach(setting => {
            if (setting.key === 'OPENAI_API_KEY') {
                document.getElementById('openai-key').placeholder = setting.is_secret ? '***' : setting.value;
            } else if (setting.key === 'GOOGLE_MAPS_API_KEY') {
                document.getElementById('google-maps-key').placeholder = setting.is_secret ? '***' : setting.value;
            } else if (setting.key === 'GOOGLE_PLACES_API_KEY') {
                document.getElementById('google-places-key').placeholder = setting.is_secret ? '***' : setting.value;
            }
        });
        
        // Display all settings
        const allSettingsEl = document.getElementById('all-settings');
        if (settings.length > 0) {
            allSettingsEl.innerHTML = settings.map(s => `
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                        <p class="font-semibold">${s.key}</p>
                        <p class="text-sm text-gray-500">${s.description || s.category}</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="text-sm ${s.is_secret ? 'text-red-600' : 'text-gray-600'}">${s.is_secret ? '🔒 Secret' : s.value}</span>
                    </div>
                </div>
            `).join('');
        } else {
            allSettingsEl.innerHTML = '<p class="text-gray-500">Még nincsenek beállítások</p>';
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

async function saveAPIKeys() {
    const openaiKey = document.getElementById('openai-key').value;
    const googleMapsKey = document.getElementById('google-maps-key').value;
    const googlePlacesKey = document.getElementById('google-places-key').value;
    
    try {
        const promises = [];
        
        if (openaiKey) {
            promises.push(fetch(`${ADMIN_API}/settings`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    key: 'OPENAI_API_KEY',
                    value: openaiKey,
                    category: 'api_keys',
                    description: 'OpenAI API kulcs AI tartalom generáláshoz',
                    is_secret: true
                })
            }));
        }
        
        if (googleMapsKey) {
            promises.push(fetch(`${ADMIN_API}/settings`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    key: 'GOOGLE_MAPS_API_KEY',
                    value: googleMapsKey,
                    category: 'api_keys',
                    description: 'Google Maps API kulcs',
                    is_secret: true
                })
            }));
        }
        
        if (googlePlacesKey) {
            promises.push(fetch(`${ADMIN_API}/settings`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    key: 'GOOGLE_PLACES_API_KEY',
                    value: googlePlacesKey,
                    category: 'api_keys',
                    description: 'Google Places API kulcs',
                    is_secret: true
                })
            }));
        }
        
        await Promise.all(promises);
        alert('✅ API kulcsok sikeresen mentve!');
        
        // Clear input fields
        document.getElementById('openai-key').value = '';
        document.getElementById('google-maps-key').value = '';
        document.getElementById('google-places-key').value = '';
        
        loadSettings();
    } catch (error) {
        console.error('Error saving API keys:', error);
        alert('❌ Hiba történt a mentés során');
    }
}

// Prompts
let editingPromptId = null;

async function loadPrompts() {
    try {
        const response = await fetch(`${ADMIN_API}/prompts`);
        const prompts = await response.json();
        
        const promptsListEl = document.getElementById('prompts-list');
        if (prompts.length > 0) {
            promptsListEl.innerHTML = prompts.map(p => `
                <div class="p-4 bg-gray-50 rounded-lg border ${p.is_default ? 'border-purple-500' : 'border-gray-200'}">
                    <div class="flex items-start justify-between">
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-2">
                                <h4 class="font-bold">${p.name}</h4>
                                ${p.is_default ? '<span class="px-2 py-1 text-xs bg-purple-100 text-purple-600 rounded-full">Alapértelmezett</span>' : ''}
                                ${p.is_active ? '<span class="px-2 py-1 text-xs bg-green-100 text-green-600 rounded-full">Aktív</span>' : '<span class="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">Inaktív</span>'}
                            </div>
                            <p class="text-sm text-gray-600 mb-2">Nyelv: ${p.language.toUpperCase()} | Típus: ${p.prompt_type}</p>
                            <div class="mt-2 p-3 bg-white rounded text-sm font-mono overflow-x-auto max-h-24 overflow-y-auto">
                                ${p.prompt_text.substring(0, 200)}${p.prompt_text.length > 200 ? '...' : ''}
                            </div>
                        </div>
                        <div class="ml-4 flex space-x-2">
                            <button onclick="editPrompt(${p.id})" class="px-3 py-1 text-sm bg-blue-100 text-blue-600 rounded hover:bg-blue-200">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button onclick="deletePrompt(${p.id})" class="px-3 py-1 text-sm bg-red-100 text-red-600 rounded hover:bg-red-200">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            promptsListEl.innerHTML = '<p class="text-gray-500">Még nincsenek prompt sablonok</p>';
        }
    } catch (error) {
        console.error('Error loading prompts:', error);
    }
}

function showPromptEditor(promptId = null) {
    editingPromptId = promptId;
    document.getElementById('prompt-editor').classList.remove('hidden');
    
    if (promptId) {
        // Load existing prompt
        fetch(`${ADMIN_API}/prompts/${promptId}`)
            .then(r => r.json())
            .then(prompt => {
                document.getElementById('prompt-name').value = prompt.name;
                document.getElementById('prompt-language').value = prompt.language;
                document.getElementById('prompt-text').value = prompt.prompt_text;
                document.getElementById('prompt-active').checked = prompt.is_active;
                document.getElementById('prompt-default').checked = prompt.is_default;
            });
    } else {
        // Clear form
        document.getElementById('prompt-name').value = '';
        document.getElementById('prompt-language').value = 'hu';
        document.getElementById('prompt-text').value = '';
        document.getElementById('prompt-active').checked = true;
        document.getElementById('prompt-default').checked = false;
    }
}

function closePromptEditor() {
    document.getElementById('prompt-editor').classList.add('hidden');
    editingPromptId = null;
}

async function savePrompt() {
    const promptData = {
        name: document.getElementById('prompt-name').value,
        language: document.getElementById('prompt-language').value,
        prompt_type: 'generation',
        prompt_text: document.getElementById('prompt-text').value,
        is_active: document.getElementById('prompt-active').checked,
        is_default: document.getElementById('prompt-default').checked
    };
    
    try {
        let url = `${ADMIN_API}/prompts`;
        let method = 'POST';
        
        if (editingPromptId) {
            url = `${ADMIN_API}/prompts/${editingPromptId}`;
            method = 'PUT';
        }
        
        const response = await fetch(url, {
            method: method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(promptData)
        });
        
        if (response.ok) {
            alert('✅ Prompt sikeresen mentve!');
            closePromptEditor();
            loadPrompts();
        } else {
            alert('❌ Hiba történt a mentés során');
        }
    } catch (error) {
        console.error('Error saving prompt:', error);
        alert('❌ Hiba történt a mentés során');
    }
}

async function editPrompt(promptId) {
    showPromptEditor(promptId);
}

async function deletePrompt(promptId) {
    if (!confirm('Biztosan törölni szeretnéd ezt a promptot?')) return;
    
    try {
        const response = await fetch(`${ADMIN_API}/prompts/${promptId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('✅ Prompt törölve!');
            loadPrompts();
        }
    } catch (error) {
        console.error('Error deleting prompt:', error);
    }
}

// Websites
async function loadWebsites() {
    try {
        const response = await fetch(`${API_BASE}/generator/websites`);
        const websites = await response.json();
        
        const websitesListEl = document.getElementById('websites-list');
        if (websites.length > 0) {
            websitesListEl.innerHTML = websites.map(w => `
                <div class="p-4 bg-gray-50 rounded-lg">
                    <div class="flex items-start justify-between">
                        <div>
                            <h4 class="font-bold text-lg">${w.business_name}</h4>
                            <p class="text-sm text-gray-600">${w.address || 'Nincs cím'}</p>
                            <div class="mt-2 flex items-center space-x-3 text-sm">
                                <span class="px-2 py-1 bg-blue-100 text-blue-600 rounded">${w.language.toUpperCase()}</span>
                                <span class="px-2 py-1 bg-green-100 text-green-600 rounded">${w.status}</span>
                                <span class="text-gray-500">${new Date(w.created_at).toLocaleDateString('hu')}</span>
                            </div>
                        </div>
                        ${w.published_url ? `<a href="${w.published_url}" target="_blank" class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700">
                            <i class="fas fa-external-link-alt mr-2"></i>Megtekintés
                        </a>` : ''}
                    </div>
                </div>
            `).join('');
        } else {
            websitesListEl.innerHTML = '<p class="text-gray-500">Még nincsenek generált weboldalak</p>';
        }
    } catch (error) {
        console.error('Error loading websites:', error);
    }
}

// Leads
async function loadLeads() {
    try {
        const response = await fetch(`${API_BASE}/leads/`);
        const leads = await response.json();
        
        const leadsListEl = document.getElementById('leads-list');
        if (leads.length > 0) {
            leadsListEl.innerHTML = `
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Név</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Telefon</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Forrás</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Státusz</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Dátum</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        ${leads.map(l => `
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${l.name}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${l.email}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${l.phone || '-'}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${l.source}</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2 py-1 text-xs rounded-full ${l.status === 'new' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}">${l.status}</span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${new Date(l.created_at).toLocaleDateString('hu')}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } else {
            leadsListEl.innerHTML = '<p class="text-gray-500">Még nincsenek leadek</p>';
        }
    } catch (error) {
        console.error('Error loading leads:', error);
    }
}

// Test & Preview
async function testGenerateWebsite() {
    const businessName = document.getElementById('test-business-name').value;
    const address = document.getElementById('test-address').value;
    const language = document.getElementById('test-language').value;
    
    if (!businessName || !address) {
        alert('Kérlek töltsd ki a vállalkozás nevét és címét!');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/generator/generate`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                business_name: businessName,
                address: address,
                language: language,
                include_widgets: true
            })
        });
        
        const result = await response.json();
        
        document.getElementById('test-result').classList.remove('hidden');
        document.getElementById('test-output').innerHTML = `
            <div class="space-y-3">
                <div>
                    <p class="font-semibold">✅ Sikeres generálás!</p>
                    <p class="text-sm text-gray-600">ID: ${result.id}</p>
                </div>
                <div>
                    <p class="font-semibold">Vállalkozás:</p>
                    <p class="text-sm">${result.business_name}</p>
                </div>
                <div>
                    <p class="font-semibold">Nyelv:</p>
                    <p class="text-sm">${result.language.toUpperCase()}</p>
                </div>
                <div>
                    <p class="font-semibold">Státusz:</p>
                    <p class="text-sm">${result.status}</p>
                </div>
                ${result.published_url ? `
                    <div>
                        <a href="${result.published_url}" target="_blank" class="inline-block px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 mt-2">
                            <i class="fas fa-external-link-alt mr-2"></i>Weboldal Megtekintése
                        </a>
                    </div>
                ` : ''}
            </div>
        `;
    } catch (error) {
        console.error('Error generating website:', error);
        alert('❌ Hiba történt a weboldal generálása során');
    }
}

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
