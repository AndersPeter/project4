document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('[data-post-id]');
    
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.dataset.postId;
            const content = button.dataset.content
            const userName = button.dataset.user
            edit_post(content, postId, userName)
        });
    });


    // Edit post function
    function edit_post(content, postId, userName) {

        //orignial post
        const post = document.getElementById(postId)

        //Content of original post
        const contentOfPost = content

        //Create div and textarea

        const div = document.createElement('div');
        div.id = postId;
        div.classList.add('border', 'm-2', 'p-3');

        const newTextarea = document.createElement('textarea');
        newTextarea.id = postId;
        newTextarea.classList.add('form-control', 'textarea-style');
        newTextarea.autofocus = true;

        const saveButton = document.createElement('button')
        saveButton.textContent = 'Save';
        saveButton.dataset.url = "edit_post";
        saveButton.classList.add('btn', 'btn-success')
        saveButton.addEventListener('click', () => {
            save(newTextarea, post, postId, userName)
            saveButton.remove();
        });
        
        div.appendChild(newTextarea)
        div.appendChild(saveButton)

        //Original content in textarea
        newTextarea.value = contentOfPost
        
        //replace post with textarea
        post.replaceWith(div)    
    };

    function save(newTextarea, post, postId, userName) {
        console.log(newTextarea)
        console.log(post)
        console.log(postId)

        const newText = newTextarea.value

        //Define new post 
        const newDiv = document.createElement('div');
        newDiv.id = postId;
        newDiv.classList.add('border', 'm-2', 'p-3');

        //Update date - Edited on
        const now = new Date();
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric', 
            hour: 'numeric', 
            minute: 'numeric', 
            hour12: true 
        };
        
        const formattedDate = now.toLocaleString('en-US', options);
        
        const profileUrl = `/profile/${postId}`;

        const newElements = `
        <h4>${ newText }</h4>
        <p>By <a href="${profileUrl}">${userName}</a> on ${formattedDate}</p>
        <button class="btn btn-primary" data-post-id="${postId}" data-content="${newText}">Edit</button>
        `;

        newDiv.innerHTML = newElements;

        const div = document.getElementById(postId)

        div.replaceWith(newDiv);

        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}`);
            if(parts.length == 2) return parts.pop().split(';').shift();
        }
        
        // Send a POST request to the URL
        fetch(`edit-post/${postId}`, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")}, //cookie added to fetch
            //add new text
            body: JSON.stringify({
                content: newText
            })
        })
        .then(response => response.json())
        .then(result => content.innerHTML = result.data)
    };
});
