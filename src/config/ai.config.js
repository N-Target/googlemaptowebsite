/**
 * AI Service Configuration
 * Manages AI model selection based on task complexity
 */

class AIConfig {
  constructor() {
    this.models = {
      simple: {
        name: 'gemini-flash',
        provider: 'google',
        tokenCost: 0.001,
        maxTokens: 8000
      },
      complex: {
        name: 'gpt-4o',
        provider: 'openai',
        tokenCost: 0.01,
        maxTokens: 128000
      }
    };
    
    this.tokenThreshold = parseInt(process.env.TOKEN_THRESHOLD) || 1000;
  }

  /**
   * Select appropriate AI model based on task complexity
   * @param {string} taskType - Type of task (e.g., 'copywriting', 'analysis', 'simple_text')
   * @param {number} estimatedTokens - Estimated token usage
   * @returns {Object} Selected model configuration
   */
  selectModel(taskType, estimatedTokens = 0) {
    const complexTasks = ['copywriting', 'trend_analysis', 'design_generation', 'complex_logic'];
    const isComplex = complexTasks.includes(taskType) || estimatedTokens > this.tokenThreshold;
    
    return isComplex ? this.models.complex : this.models.simple;
  }

  /**
   * Get all available models
   */
  getAllModels() {
    return this.models;
  }

  /**
   * Calculate token cost
   */
  calculateCost(tokens, modelType = 'simple') {
    const model = this.models[modelType];
    return tokens * model.tokenCost;
  }
}

module.exports = new AIConfig();
