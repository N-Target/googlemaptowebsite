const { GoogleGenerativeAI } = require('@google/generative-ai');
const OpenAI = require('openai');
const aiConfig = require('../config/ai.config');

class AIService {
  constructor() {
    this.gemini = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }

  /**
   * Generate content using appropriate AI model
   * @param {string} prompt - The prompt for content generation
   * @param {string} taskType - Type of task
   * @param {Object} options - Additional options
   */
  async generateContent(prompt, taskType = 'simple_text', options = {}) {
    const startTime = Date.now();
    const modelConfig = aiConfig.selectModel(taskType, options.estimatedTokens);
    
    let result;
    let tokensUsed = 0;

    try {
      if (modelConfig.provider === 'google') {
        result = await this.generateWithGemini(prompt, modelConfig, options);
        tokensUsed = result.tokensUsed || 0;
      } else {
        result = await this.generateWithOpenAI(prompt, modelConfig, options);
        tokensUsed = result.tokensUsed || 0;
      }

      const generationTime = Date.now() - startTime;

      return {
        content: result.content,
        metadata: {
          model: modelConfig.name,
          provider: modelConfig.provider,
          tokensUsed,
          generationTime,
          cost: aiConfig.calculateCost(tokensUsed, taskType === 'simple_text' ? 'simple' : 'complex')
        }
      };
    } catch (error) {
      console.error('AI Generation Error:', error);
      throw new Error(`Failed to generate content: ${error.message}`);
    }
  }

  /**
   * Generate content using Gemini
   */
  async generateWithGemini(prompt, modelConfig, options) {
    const model = this.gemini.getGenerativeModel({ model: 'gemini-pro' });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    return {
      content: text,
      tokensUsed: this.estimateTokens(text)
    };
  }

  /**
   * Generate content using OpenAI
   */
  async generateWithOpenAI(prompt, modelConfig, options) {
    const response = await this.openai.chat.completions.create({
      model: modelConfig.name,
      messages: [{ role: 'user', content: prompt }],
      max_tokens: options.maxTokens || 2000,
      temperature: options.temperature || 0.7
    });

    return {
      content: response.choices[0].message.content,
      tokensUsed: response.usage.total_tokens
    };
  }

  /**
   * Estimate tokens for a given text (rough approximation)
   */
  estimateTokens(text) {
    return Math.ceil(text.length / 4);
  }

  /**
   * Generate website copy for a business
   */
  async generateWebsiteCopy(businessData, language = 'hu') {
    const prompt = this.buildWebsiteCopyPrompt(businessData, language);
    return this.generateContent(prompt, 'copywriting', { estimatedTokens: 2000 });
  }

  /**
   * Build prompt for website copy generation
   */
  buildWebsiteCopyPrompt(businessData, language) {
    const languageMap = {
      hu: 'Hungarian',
      en: 'English',
      de: 'German'
    };

    return `
Generate professional, luxury-positioned website copy in ${languageMap[language]} for the following business:

Business Name: ${businessData.businessName}
Business Type: ${businessData.businessType}
Address: ${businessData.address || 'N/A'}
Rating: ${businessData.rating || 'N/A'} stars
Services: ${businessData.services ? businessData.services.join(', ') : 'N/A'}

Create:
1. A compelling headline (max 10 words)
2. A detailed description (2-3 paragraphs)
3. List of key features/benefits (5-7 items)
4. Call-to-action text

Focus on:
- Luxury positioning
- Local relevance
- Trust and credibility
- Emotional connection
- Clear value proposition

Return the response in JSON format with keys: headline, description, features, cta
`;
  }

  /**
   * Analyze global trends for a specific industry
   */
  async analyzeTrends(industry, region = 'EU') {
    const prompt = `
Analyze current global trends for the ${industry} industry in ${region}.
Focus on:
1. Emerging consumer preferences
2. Technology adoption
3. Marketing strategies
4. Competitive landscape
5. Growth opportunities

Provide actionable insights in JSON format.
`;
    return this.generateContent(prompt, 'trend_analysis', { estimatedTokens: 3000 });
  }
}

module.exports = new AIService();
