import React, { useState } from 'react';
import { useDeleteTodoMutation, useUpdateTodoMutation } from '../api/apiSlice';
import Modal from './Modal';

type Todo = {
    id?: number;
    title: string;
    description: string;
    completed: boolean;
};

type TodoProps = {
    todo: Todo;
};
const Todo: React.FC<TodoProps> = ({ todo }: TodoProps) => {
    const [updateTodo] = useUpdateTodoMutation();
    const [deleteTodo] = useDeleteTodoMutation();
    const [editTodo, setEditTodo] = useState<Todo | null>(null);

    const handleClick = async () => {
        await updateTodo({ id: todo.id, completed: !todo.completed });
    };

    const handleDelete = async () => {
        const confirm = window.confirm('Confirm delete');
        if (confirm && todo.id) {
            await deleteTodo({ id: todo.id });
        }
    };
    return (
        <>
            <div style={{ display: 'flex' }}>
                <input type='checkbox' checked={todo.completed} onChange={handleClick} />
                <p>
                    {todo.title} | {todo.description}
                </p>
            </div>

            <div style={{ display: 'flex' }}>
                <button onClick={handleDelete}>Delete</button>
                <button onClick={() => setEditTodo(todo)}>Edit</button>
            </div>

            {editTodo && <Modal todo={editTodo} closeModal={() => setEditTodo(null)} />}
        </>
    );
};

export default Todo;
