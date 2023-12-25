function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const buttons = document.getElementsByClassName('vote');

for (let button of buttons) {
    const [vote, counter] = button.children;
    console.log(button.dataset)
    button.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('type', button.dataset.type)
        formData.append('id', button.dataset.id)

        const request = new Request('/vote', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
                if (button.classList.contains('voted')) {
                    button.classList.replace('voted', 'vote');
                    button.classList.replace('btn-success', 'btn-danger');
                    counter.classList.replace('btn-info', 'bg-warning');
                } else {
                    button.classList.replace('vote', 'voted');
                    button.classList.replace('btn-danger', 'btn-success');
                    counter.classList.replace('bg-warning', 'btn-info');
                }
            })
            .catch((err) => {
                window.location = '';
            })
    })
}

const correctnesses = document.getElementsByClassName('correctness');

for (const correctness of correctnesses) {
    correctness.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('answer_id', correctness.dataset.answerId)
        formData.append('question_id', correctness.dataset.questionId)

        const request = new Request('/correctness', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log(data.success)
            })
    })
}