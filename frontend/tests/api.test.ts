import { describe, it, expect, vi } from 'vitest'
import { api } from '../src/lib/api'

describe('api client', () => {
  it('parses JSON and returns typed data', async () => {
    const mockResponse = { foo: 'bar' }
    globalThis.fetch = vi.fn(() => Promise.resolve(new Response(JSON.stringify(mockResponse), { status: 200 }))) as any

    const data = await api.get<{ foo: string }>('/test')
    expect(data).toEqual(mockResponse)
  })

  it('throws on non-ok response with message', async () => {
    globalThis.fetch = vi.fn(() => Promise.resolve(new Response(JSON.stringify({ detail: 'bad' }), { status: 400, statusText: 'Bad' }))) as any
    await expect(api.get('/bad')).rejects.toThrow(/bad|Bad/)
  })
})
