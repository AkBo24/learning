import React from 'react';

type Todo = {
    id?: number;
    title: string;
    description?: string;
    completed: boolean;
};

type TodoProps = {
    todo: Todo;
};
const Todo: React.FC<TodoProps> = ({ todo }: TodoProps) => {
    return <p>{todo.title}</p>;
};

export default Todo;
