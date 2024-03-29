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

const handleLikeClick = (buttonId) => {
    console.log(buttonId);

    const likeButton = document.getElementById(buttonId);
    const likeIcon = likeButton.querySelector('i');
    likeIcon.classList.replace("fa-heart-o", "fa-heart");
    
    const csrftoken = getCookie('csrftoken');

    
    const postId = buttonId.split("-").pop();
    const url = "/posts/" + postId + "/post_like/"
    // 서버에서 좋아요 api를 호출
    fetch(url, {
        method : "POST",
        mode : "same-origin",
        headers : {
        "X-CSRFToken": csrftoken
        }
    })
    .then(response => response.json())

    // 결과를 받고 html 좋아요 표시를 변경
    .then(data =>{
        if (data.result === "like") {
            // 좋아요 세팅 흰색 -> 검은색
            likeIcon.classList.replace("fa-heart-o", "fa-heart");
        } else {
            // 좋아요 취소 검은색 -> 흰색
            likeIcon.classList.replace("fa-heart", "fa-heart-o");
        }
    });
}
