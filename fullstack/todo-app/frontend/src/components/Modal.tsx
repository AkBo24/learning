import React, { useState } from 'react';
import Todo from './Todo';
import { useUpdateTodoMutation } from '../api/apiSlice';

const Modal: React.FC<{ todo: Todo; closeModal: () => void }> = ({
    todo,
    closeModal,
}) => {
    const [updateTodo] = useUpdateTodoMutation();

    const [todoTitle, setTodoTitle] = useState<string>(todo.title);
    const [todoDescription, setTodoDescription] = useState<string>(todo.description);

    const handleSubmit = async () => {
        if (!todoTitle) {
            alert('Title required');
            return;
        }
        if (!todoDescription) {
            alert('Description required');
            return;
        }
        await updateTodo({
            ...todo,
            title: todoTitle,
            description: todoDescription,
        });
        closeModal();
    };
    return (
        <div
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                background: 'rgba(0, 0, 0, 0.5)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: 1000,
            }}>
            <form
                style={{
                    background: 'white' /* White background */,
                    padding: '2rem' /* Add some padding */,
                    borderRadius: '8px' /* Rounded corners */,
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)' /* Subtle shadow */,
                    width: '90%' /* Responsive width */,
                    maxWidth: '500px' /* Maximum width */,
                    textAlign: 'center' /* Center the text */,
                }}
                onSubmit={handleSubmit}>
                <h3>Edit Todo</h3>
                <p>{todo.title}</p>

                <div>
                    <label htmlFor='new-todo-title'>Title</label>
                    <input
                        onChange={(e) => setTodoTitle(e.target.value)}
                        id='new-todo-title'
                        value={todoTitle}
                        placeholder='Enter new todo…'
                    />
                </div>

                <div>
                    <label htmlFor='new-todo-description'>Description</label>
                    <textarea
                        onChange={(e) => setTodoDescription(e.target.value)}
                        id='new-todo-description'
                        value={todoDescription}
                        placeholder='Enter todo details'
                    />
                </div>

                <button onClick={closeModal}>Cancel</button>
                <button type='submit'>Save</button>
            </form>
        </div>
    );
};

export default Modal;
