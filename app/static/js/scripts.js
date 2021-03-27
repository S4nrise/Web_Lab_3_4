const form = document.querySelector('#ajax-form');
const titleInput = document.querySelector('#title-input-ajax');
const titleDesc = document.querySelector('#title-description');
const todosList = document.querySelector('#todos');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
        const response = await fetch('/api/todos', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                todo_name: titleInput.value,
                todo_description: titleDesc.value,
            }),
        });
        if (!response.ok) {
            alert(await response.text());
            return;
        }
        const newTodo = await response.json();
        const newListItem = document.createElement('li');

        newListItem.classList.add('list-group-item');
        newListItem.setAttribute('data-todo-id', newTodo.todo_id);

        const newListBlockItem = document.createElement('div');
        newListBlockItem.classList.add('todo-item');

        const itemLabel = document.createElement('label');
        itemLabel.setAttribute('for', newTodo.todo_id);
        itemLabel.textContent = newTodo.name;

        const itemBlock = document.createElement('div');
        itemBlock.classList.add('todo-description');
        itemBlock.setAttribute('id', newTodo.todo_id);
        itemBlock.textContent = newTodo.description;

        const editButton = document.createElement('button');
        editButton.type = 'button';
        editButton.classList.add('btn', 'btn-outline-success', 'btn-sm');
        editButton.textContent = '✎';
        editButton.setAttribute('onclick', `change_status_todo(${newTodo.todo_id})`);

        const deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.classList.add('btn', 'btn-outline-danger', 'btn-sm');
        deleteButton.textContent = '❌';
        deleteButton.setAttribute('onclick', `delete_todo(${newTodo.todo_id})`);

        newListBlockItem.appendChild(itemLabel);
        newListBlockItem.appendChild(itemBlock);
        newListBlockItem.appendChild(editButton);
        newListBlockItem.appendChild(deleteButton);

        newListItem.appendChild(newListBlockItem);
        todosList.appendChild(newListItem);
    } catch (e) {
        alert(e.message);
    }
});

async function delete_todo(todoId) {
    try {
        const response = await fetch(`/api/todos/${todoId}/delete`, {
            method: 'DELETE',
            credentials: 'same-origin',
        });
        if (!response.ok) {
            alert(await response.text());
            if (response.status === 401) {
                window.location = '/login';
            }
            return;
        }
        document.querySelector(`li[data-todo-id='${todoId}']`).remove();
    } catch (e) {
        alert(e.message);
    }
}

async function change_status_todo(todoId) {
    try {
        const response = await fetch(`/api/todos/${todoId}`, {
            method: 'POST',
            credentials: 'same-origin',
        });
        if (!response.ok) {
            alert(await response.text());
            if (response.status === 401) {
                window.location = '/login';
            }
            return;
        }
        const editedTodo = await response.json();
        var el = document.querySelector(`li[data-todo-id='${todoId}']`);
        if(editedTodo.is_done) {
            el.classList.add("ended");
            el.querySelector("label").innerHTML = editedTodo.name + "<span style='color: #ff0000;'>(ended)</span>";
        } else {
            el.classList.remove("ended");
            el.querySelector("label").innerHTML = editedTodo.name;
        }
    } catch (e) {
        alert(e.message);
    }
}

function filter_todo(item) {
    const todosItems = document.getElementsByClassName('list-group-item');
    if(item.checked) {
        for(item of todosItems) {
            if(item.classList.contains("ended")) {
                item.classList.add("hidden");
            }
        }
    } else {
        for(item of todosItems) {
            if(item.classList.contains("hidden")) {
                item.classList.remove("hidden");
            }
        }
    }
}