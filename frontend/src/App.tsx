import axios from 'axios'
import { useCallback, useEffect, useState } from 'react' // Добавили useCallback
import { getBooks, getMyLoans, rentBook, type Book, type Loan } from './api' // Добавили getMyLoans
import './App.css'
import Auth from './Auth'

function App() {
	const [books, setBooks] = useState<Book[]>([])
	const [token, setToken] = useState<string | null>(
		localStorage.getItem('token'),
	)
	const [loading, setLoading] = useState(!!token)

	// Управление вкладками
	const [activeTab, setActiveTab] = useState<'all' | 'my'>('all')
	const [myLoans, setMyLoans] = useState<Loan[]>([])

	// Выход из системы
	const handleLogout = useCallback(() => {
		localStorage.removeItem('token')
		setToken(null)
		setBooks([])
		setActiveTab('all')
	}, [])

	// Загрузка всех книг
	const fetchBooks = useCallback(async () => {
		setLoading(true)
		try {
			const res = await getBooks()
			setBooks(res.data)
		} catch (err: unknown) {
			if (axios.isAxiosError(err) && err.response?.status === 401) {
				handleLogout()
			}
		} finally {
			setLoading(false)
		}
	}, [handleLogout])

	// Загрузка ЛК
	const fetchMyLoans = useCallback(async () => {
		try {
			const res = await getMyLoans()
			setMyLoans(res.data)
		} catch (err) {
			console.error('Ошибка загрузки ЛК', err)
		}
	}, [])

	useEffect(() => {
		const loadData = async () => {
			if (!token) return

			// Включаем индикатор загрузки
			setLoading(true)

			try {
				// Запускаем оба запроса одновременно для скорости
				await Promise.all([fetchBooks(), fetchMyLoans()])
			} catch (err) {
				console.error('Ошибка при первичной загрузке данных', err)
			} finally {
				// Выключаем загрузку в любом случае
				setLoading(false)
			}
		}

		loadData()
		// Добавляем зависимости, чтобы избежать ворнингов ESLint
	}, [token, fetchBooks, fetchMyLoans])

	// Логика бронирования
	const handleReserve = async (bookId: number) => {
		try {
			await rentBook(bookId)
			alert('Книга забронирована!')
			await fetchBooks() // Обновляем каталог
		} catch (err: unknown) {
			if (axios.isAxiosError(err)) {
				alert(err.response?.data?.error || 'Ошибка бронирования')
			}
		}
	}

	if (!token) return <Auth onLoginSuccess={t => setToken(t)} />

	return (
		<div className='container'>
			<header className='header'>
				<h1>📚 СКФУ: Библиотека</h1>
				<div className='nav-buttons'>
					<button
						className={`nav-btn ${activeTab === 'all' ? 'active' : ''}`}
						onClick={() => setActiveTab('all')}
					>
						Каталог
					</button>
					<button
						className={`nav-btn ${activeTab === 'my' ? 'active' : ''}`}
						onClick={() => {
							setActiveTab('my')
							fetchMyLoans()
						}}
					>
						Мои книги
					</button>
				</div>
				<button className='btn-logout' onClick={handleLogout}>
					Выйти
				</button>
			</header>

			{loading && activeTab === 'all' ? (
				<div style={{ color: 'white', textAlign: 'center', marginTop: '50px' }}>
					Загрузка полки...
				</div>
			) : activeTab === 'all' ? (
				<div className='book-grid'>
					{books.map(book => (
						<div key={book.id} className='book-card'>
							<h3>{book.title}</h3>
							<p>Автор: {book.author}</p>
							<div
								className='status'
								style={{ color: book.is_available ? '#4caf50' : '#f44336' }}
							>
								<span
									className='dot'
									style={{
										background: book.is_available ? '#4caf50' : '#f44336',
									}}
								></span>
								{book.is_available ? 'Доступна' : 'Забронирована'}
							</div>
							<button
								className='btn-reserve'
								onClick={() => handleReserve(book.id)}
								disabled={!book.is_available}
							>
								{book.is_available ? 'Забронировать' : 'Уже занята'}
							</button>
						</div>
					))}
				</div>
			) : (
				<div className='my-loans-section'>
					<div className='stats-bar'>
						<div className='stat-item'>
							Бронь:{' '}
							<strong>
								{myLoans.filter(l => l.status === 'reserved').length}
							</strong>
						</div>
						<div className='stat-item'>
							На руках:{' '}
							<strong>
								{myLoans.filter(l => l.status === 'issued').length}
							</strong>
						</div>
					</div>

					<div className='book-grid'>
						{myLoans.length === 0 ? (
							<p
								style={{
									color: '#777',
									textAlign: 'center',
									gridColumn: '1/-1',
								}}
							>
								У вас пока нет выбранных книг
							</p>
						) : (
							myLoans.map(loan => {
								// Проверяем на просрочку
								// Превращаем строку даты "07.04.2026" в объект даты для сравнения
								const parts = loan.deadline ? loan.deadline.split('.') : []
								const deadlineDate = loan.deadline
									? new Date(`${parts[2]}-${parts[1]}-${parts[0]}`)
									: null
								const isOverdue =
									loan.status === 'issued' &&
									deadlineDate &&
									deadlineDate < new Date()

								return (
									<div
										key={loan.id}
										className={`book-card ${isOverdue ? 'overdue-card' : ''}`}
										style={{
											borderLeft: isOverdue
												? '6px solid #ff4d4d'
												: loan.status === 'reserved'
													? '4px solid #ff9800'
													: '4px solid #4caf50',
										}}
									>
										<h3>{loan.book_title}</h3>
										<p>Автор: {loan.author}</p>

										<p className='loan-status'>
											Статус:
											{isOverdue ? (
												<strong style={{ color: '#ff4d4d' }}>
													{' '}
													🛑 ПРОСРОЧЕНО
												</strong>
											) : (
												<strong>
													{loan.status === 'reserved'
														? ' 🟠 Ожидает получения'
														: ' 🟢 На руках'}
												</strong>
											)}
										</p>

										<p className='loan-date'>Взято: {loan.date}</p>

										{loan.status === 'issued' && loan.deadline && (
											<p
												className={`loan-deadline ${isOverdue ? 'text-danger' : ''}`}
											>
												📅 Вернуть до: <strong>{loan.deadline}</strong>
											</p>
										)}

										{isOverdue && (
											<div className='overdue-badge'>
												Срочно верните книгу в библиотеку!
											</div>
										)}
									</div>
								)
							})
						)}
					</div>
				</div>
			)}
		</div>
	)
}

export default App
