const aiConfig = require('../src/config/ai.config');

describe('AI Configuration', () => {
  test('should select Gemini for simple tasks', () => {
    const model = aiConfig.selectModel('simple_text', 500);
    expect(model.provider).toBe('google');
    expect(model.name).toBe('gemini-flash');
  });

  test('should select GPT-4o for complex tasks', () => {
    const model = aiConfig.selectModel('copywriting', 100);
    expect(model.provider).toBe('openai');
    expect(model.name).toBe('gpt-4o');
  });

  test('should select GPT-4o for high token count', () => {
    const model = aiConfig.selectModel('simple_text', 2000);
    expect(model.provider).toBe('openai');
    expect(model.name).toBe('gpt-4o');
  });

  test('should calculate cost correctly', () => {
    const simpleCost = aiConfig.calculateCost(1000, 'simple');
    expect(simpleCost).toBe(1); // 1000 * 0.001

    const complexCost = aiConfig.calculateCost(1000, 'complex');
    expect(complexCost).toBe(10); // 1000 * 0.01
  });

  test('should return all models', () => {
    const models = aiConfig.getAllModels();
    expect(models).toHaveProperty('simple');
    expect(models).toHaveProperty('complex');
  });
});
