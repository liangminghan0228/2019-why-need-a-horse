import BeforeTestPage from '../../src/components/BeforeTestPage'

describe('BeforeTestPage.vue', () => {
  it('has a created hook', () => {
    expect(typeof BeforeTestPage.data).toBe('function')
  })

  it('sets the correct default data', () => {
    const defaultData = BeforeTestPage.data()
    expect(defaultData.bookName).toBe('初中核心词')
  })
})