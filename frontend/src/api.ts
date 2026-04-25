import axios from 'axios'

const api = axios.create({
	baseURL: 'http://127.0.0.1:8000/api/',
})

// 🔑 токен
api.interceptors.request.use(config => {
	const token = localStorage.getItem('token')
	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}
	return config
})

// 📚 типы
export interface Book {
	id: number
	title: string
	author: string
	category_name: string
	isbn: string
	publication_year: number
	is_available: boolean
}

export interface User {
	id: number
	username: string
	email: string
	is_librarian: boolean
}

export interface Loan {
	id: number
	status: 'reserved' | 'issued' | 'returned'

	// Поля, которые ты реально используешь в map():
	book_title: string // Название книги
	author: string // Автор книги
	date: string // Дата взятия (loan_date)
	deadline: string | null // Срок возврата (return_deadline)

	// Оставляем на всякий случай, если понадобятся ID
	book?: number
	user?: number
}

// 📡 API
export const getBooks = () => api.get<Book[]>('books/')

export const registerUser = (userData: Record<string, string>) =>
	api.post('auth/users/', userData)

export const loginUser = (credentials: Record<string, string>) =>
	api.post('auth/jwt/create/', credentials)

export const getMe = () => api.get<User>('auth/users/me/')

// 🚀 ВАЖНО: правильный endpoint
export const rentBook = (bookId: number) => api.post(`loans/rent/${bookId}/`)

export const getMyLoans = () => api.get('/books/my_loans/')

export default api
