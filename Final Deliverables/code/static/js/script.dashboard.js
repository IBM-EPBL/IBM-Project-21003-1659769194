/** @jsx createElement */
/*** @jsxFrag createFragment */

const createElement = (tag, props, ...children) => {
	if (typeof tag === "function") return tag(props, ...children);
	const element = document.createElement(tag);

	Object.entries(props || {}).forEach(([name, value]) => {
		if (name.startsWith("on") && name.toLowerCase() in window)
			element.addEventListener(name.toLowerCase().substr(2), value);
		else element.setAttribute(name, value.toString());
	});

	children.forEach(child => {
		appendChild(element, child);
	});

	return element;
};

const appendChild = (parent, child) => {
	if (Array.isArray(child))
		child.forEach(nestedChild => appendChild(parent, nestedChild));
	else
		parent.appendChild(child.nodeType ? child : document.createTextNode(child));
};

const createFragment = (props, ...children) => {
	return children;
};

const displayBalance = () => {
	let val = document.querySelector("#balance")
	fetch("/api/balance")
	.then(body=>body.json())
	.then((x)=>{
		val.innerHTML=x.balance;
	})
}

const displayName = () => {
	let val = document.querySelector("#user_name")
	fetch("/api/session")
	.then(body=>body.json())
	.then((x)=>{
		if ("name" in x){
			val.innerHTML=x.name;
		} else {
			window.location = "/"
		}
	})
}

const Transaction = (props) => (
	<div class="transfer">
		<div class="transfer-logo">
			<img src="https://upload.wikimedia.org/wikipedia/commons/3/3e/Dollar_sign_in_circle.svg" />
		</div>
		<dl class="transfer-details">
			<div>
				<dt>{props? props.category : "other"}</dt>
				<dd>{props? props.category : "other"}</dd>
			</div>
			<div>
				<dt>{props? props.date : ""}</dt>
				<dd>Date payment</dd>
			</div>
		</dl>
		<div class="transfer-number">
			{props? props.amount : 0}
		</div>
	</div>
)

const reverseTransactions = () => {
	displayTransactions(displayTransactions.reverse);
}

const displayTransactions = (bool) => {
	if (bool===true) {
		displayTransactions.reverse = false;
	}
	if (bool===false){
		displayTransactions.reverse = true;
	}
	let val = document.querySelector("#balance")
	fetch("/api/expenses")
	.then(body=>body.json())
	.then((x)=>{
		let node = document.querySelector(".transfer-section")
		if (displayTransactions.reverse){
			x = x.reverse();
		}
		node
		.replaceChild(
			<div class="transfers">
				{x.map(row=>(<Transaction category={row.category} date={row.date} amount={row.amount}/>))}
			</div>
		,node.querySelector(".transfers"))
	})
}

const delParent = (e) => {
	e.currentTarget.parentElement.remove();
}

const updateBalance = (e) => {
	e.preventDefault()
	let form = event.currentTarget;
	let form_data = new FormData();
	form_data.append("category", "others")
	let yourDate = new Date()
	form_data.append("date", yourDate.toISOString().split('T')[0])
	fetch("/api/balance")
	.then(body=>body.json())
	.then((x)=>{
		form_data.append("amount", +(x.balance)-form.querySelector("input[name='amount']").value)
		fetch("/api/expenses", {
			method: "POST",
			body: form_data
		})
			.then(body=>body.json())
			.then((x)=>{
				if (!x.Success){
					//alert(x.msg);
					main();
				} else {
					window.location = "/dashboard"
				}
			})
	})
}

const addExpense = (e) => {
	e.preventDefault()
	let form = event.currentTarget;
	fetch("/api/expenses", {
		method: "POST",
		body: new FormData(form)
	})
	.then(body=>body.json())
	.then((x)=>{
		if (!x.Success){
			//alert(x.msg);
			main();
		} else {
			window.location = "/dashboard"
		}
	})
}

const openBalPopup = (e) => {
	var modal = document.getElementById("myModal");
	var btn = document.getElementById("myBtn");
	var span = document.getElementsByClassName("close")[0];
	btn.onclick = function() {
		modal.style.display = "block";
		document.querySelector("body").style.overflow="hidden";
	}
	span.onclick = function() {
		modal.style.display = "none";
		document.querySelector("body").style.overflow="unset";
	}

}

const logout = () => {
	fetch("/api/session",{
		method: "DELETE"
	})
	.then(()=>{
		window.location = "/"
	})
}

const main = () => {
	displayBalance()
	displayTransactions.reverse = true;
	displayTransactions()
	displayName()
}

window.onload = main

main()
