let toggleShowPass = (event) => {
	let x = event.currentTarget.parentElement.querySelector("input");
	if (x.type === "password") {
		x.type = "text";
	} else {
		x.type = "password";
	}
}

const submitLoginForm = (e) => {
	e.preventDefault()
	let form = event.currentTarget;
	fetch("/api/login", {
		method: "POST",
		body: new FormData(form)
	})
	.then(body=>body.json())
	.then((x)=>{
		if (!x.Success){
			alert(x.msg);
		} else {
			window.location = "/dashboard"
		}
	})
}

const submitRegisterForm = (e) => {
	e.preventDefault()
	let form = event.currentTarget;
	fetch("/api/register", {
		method: "POST",
		body: new FormData(form)
	})
	.then(body=>body.json())
	.then((x)=>{
		if (!x.Success){
			alert(x.msg);
		} else {
			window.location = "/"
		}
	})
}
