import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    const response = await fetch(`${backendUrl}/health`)
    
    if (response.ok) {
      return NextResponse.json({ status: 'ok', backend: 'connected' })
    }
    
    return NextResponse.json({ status: 'error', backend: 'disconnected' }, { status: 503 })
  } catch (error) {
    return NextResponse.json({ status: 'error', backend: 'disconnected' }, { status: 503 })
  }
}