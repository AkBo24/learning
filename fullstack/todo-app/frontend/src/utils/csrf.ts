export const getCsrfToken = () => {
    const name = 'csrftoken';
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
};
