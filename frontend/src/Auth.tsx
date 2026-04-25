import axios from 'axios'
import React, { useState } from 'react'
import { loginUser, registerUser } from './api'

const Auth = ({
	onLoginSuccess,
}: {
	onLoginSuccess: (token: string) => void
}) => {
	const [isLogin, setIsLogin] = useState(true)
	const [formData, setFormData] = useState({
		username: '',
		password: '',
		re_password: '',
		email: '',
	})

	// Переключалка режима
	const toggleMode = () => {
		setIsLogin(!isLogin)
		setFormData({ username: '', password: '', re_password: '', email: '' }) // Чистим поля
	}

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault()
		try {
			if (isLogin) {
				const res = await loginUser({
					username: formData.username,
					password: formData.password,
				})
				// SimpleJWT возвращает объект { access: "...", refresh: "..." }
				const token = res.data.access
				localStorage.setItem('token', token)
				onLoginSuccess(token)
			} else {
				// При регистрации отправляем всё (username, email, password, re_password)
				await registerUser(formData)
				alert('Регистрация успешна! Теперь войдите под своим логином.')
				setIsLogin(true)
			}
		} catch (err: unknown) {
			// Используем unknown вместо any
			console.error('Auth error:', err)

			let errorMsg = 'Ошибка доступа. Проверьте данные.'

			// Проверяем, является ли ошибка ошибкой от Axios
			if (axios.isAxiosError(err) && err.response?.data) {
				const data = err.response.data
				// Собираем ошибки из объекта (например, ошибки валидации от Django)
				errorMsg = Object.values(data).flat().join(' ')
			}

			alert(errorMsg)
		}
	}

	return (
		<div
			style={{
				maxWidth: '400px',
				margin: '50px auto',
				padding: '30px',
				border: '1px solid #ddd',
				borderRadius: '15px',
				boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
				textAlign: 'center',
			}}
		>
			<h2 style={{ marginBottom: '20px', color: '#2c3e50' }}>
				{isLogin ? '🔑 Вход в систему' : '📝 Регистрация'}
			</h2>

			<form
				onSubmit={handleSubmit}
				style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}
			>
				<input
					placeholder='Логин'
					value={formData.username}
					onChange={e => setFormData({ ...formData, username: e.target.value })}
					style={{
						padding: '12px',
						borderRadius: '5px',
						border: '1px solid #ccc',
					}}
					required
				/>

				{!isLogin && (
					<input
						type='email'
						placeholder='Email'
						value={formData.email}
						onChange={e => setFormData({ ...formData, email: e.target.value })}
						style={{
							padding: '12px',
							borderRadius: '5px',
							border: '1px solid #ccc',
						}}
						required
					/>
				)}

				<input
					type='password'
					placeholder='Пароль'
					value={formData.password}
					onChange={e => setFormData({ ...formData, password: e.target.value })}
					style={{
						padding: '12px',
						borderRadius: '5px',
						border: '1px solid #ccc',
					}}
					required
				/>

				{!isLogin && (
					<input
						type='password'
						placeholder='Повторите пароль'
						value={formData.re_password}
						onChange={e =>
							setFormData({ ...formData, re_password: e.target.value })
						}
						style={{
							padding: '12px',
							borderRadius: '5px',
							border: '1px solid #ccc',
						}}
						required
					/>
				)}

				<button
					type='submit'
					style={{
						padding: '12px',
						background: '#007bff',
						color: 'white',
						border: 'none',
						borderRadius: '5px',
						cursor: 'pointer',
						fontSize: '16px',
						fontWeight: 'bold',
					}}
				>
					{isLogin ? 'Войти' : 'Создать аккаунт'}
				</button>
			</form>

			<button
				onClick={toggleMode}
				style={{
					marginTop: '20px',
					background: 'none',
					border: 'none',
					color: '#007bff',
					cursor: 'pointer',
					textDecoration: 'underline',
				}}
			>
				{isLogin
					? 'Нет аккаунта? Зарегистрироваться'
					: 'Уже есть аккаунт? Войти'}
			</button>
		</div>
	)
}

export default Auth
