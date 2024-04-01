document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('.for_inicio');

    formulario.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(formulario);
        const correo = formData.get('correo');
        const contraseña = formData.get('contraseña');

        try {
            const response = await fetch('/', {
                method: 'POST',
                body: JSON.stringify({ correo, contraseña }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Hubo un problema al iniciar sesión');
            }

            const data = await response.json();

            if (data.redireccionar) {
                window.location.href = data.redireccionar;
            } else {
                console.error('No se proporcionó una URL de redireccionamiento válida');
            }
        } catch (error) {
            console.error('Error:', error.message);
        }
    });
});
