import React from 'react'
import { render, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { act } from 'react'
import { AuthProvider, useAuth } from '@/domains/users/auth/AuthContext'

function Consumer() {
  const { currentUser, signIn, signOut, loading } = useAuth()
  return (
    <div>
      <div data-testid="loading">{String(loading)}</div>
      <div data-testid="user">{currentUser ? currentUser.username : 'no-user'}</div>
      <button onClick={() => signIn('a', 'b')}>signin</button>
      <button onClick={() => signOut()}>signout</button>
    </div>
  )
}

describe('AuthContext', () => {
  it('signs in and signs out', async () => {
    // mock login response
    globalThis.fetch = vi.fn((url: string) => {
      const urlStr = String(url);
      if (urlStr.includes('/auth/login')) {
        return Promise.resolve(new Response(JSON.stringify({ access_token: 'token' }), { status: 200 }));
      }
      if (urlStr.includes('/users/me')) {
        return Promise.resolve(new Response(JSON.stringify({ id: 1, username: 'bob', email: 'a@b' }), { status: 200 }));
      }
      if (urlStr.includes('/auth/logout')) {
        return Promise.resolve(new Response(null, { status: 200 }));
      }
      return Promise.resolve(new Response(null, { status: 404 }));
    }) as any;

    const { getByText, getByTestId } = render(
      <AuthProvider>
        <Consumer />
      </AuthProvider>,
    )

    // call sign in — wrap in act so React knows we're performing state updates in the test
    await act(async () => {
      getByText('signin').click()
    })

    // wait for user to be populated
    await waitFor(() => expect(getByTestId('user').textContent).toBe('bob'))

    // sign out — also wrap in act to silence warnings about state updates
    await act(async () => {
      getByText('signout').click()
    })
    await waitFor(() => expect(getByTestId('user').textContent).toBe('no-user'))
  })
})
