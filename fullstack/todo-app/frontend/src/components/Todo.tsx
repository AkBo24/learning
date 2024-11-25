import React, { useState } from 'react';
import { useUpdateTodoMutation } from '../api/apiSlice';
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
    const [editTodo, setEditTodo] = useState<Todo | null>(null);

    const handleClick = async () => {
        await updateTodo({ id: todo.id, completed: !todo.completed });
    };
    return (
        <>
            <div style={{ display: 'flex' }}>
                <input type='checkbox' checked={todo.completed} onChange={handleClick} />
                <p>
                    {todo.title} | {todo.description}
                </p>
            </div>
            <button onClick={() => setEditTodo(todo)}>Edit</button>

            {editTodo && <Modal todo={editTodo} closeModal={() => setEditTodo(null)} />}
        </>
    );
};

export default Todo;
