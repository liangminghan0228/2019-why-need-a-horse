import BeforeStudying from '../../src/components/BeforeStudying'

describe('BeforeStudying.vue', () => {
  it('has a created hook', () => {
    expect(typeof BeforeStudying.data).toBe('function')
  })

  it('sets the correct default data', () => {
    const defaultData = BeforeStudying.data()
    expect(defaultData.showStudying).toBe(true)
  })
})