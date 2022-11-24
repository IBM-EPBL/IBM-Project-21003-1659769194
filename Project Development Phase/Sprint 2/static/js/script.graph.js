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
	fetch("http://localhost:5000/api/balance")
	.then(body=>body.json())
	.then((x)=>{
		val.innerHTML=x.balance;
	})
}

const displayName = () => {
	let val = document.querySelector("#user_name")
	fetch("http://localhost:5000/api/session")
	.then(body=>body.json())
	.then((x)=>{
		if ("name" in x){
			val.innerHTML=x.name;
		} else {
			window.location = "http://localhost:5000"
		}
	})
}

const Transaction = (props) => (
	<div class="transfer">
		<div class="transfer-logo">
			<img src="https://assets.codepen.io/285131/apple.svg" />
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

const displayTransactions = () => {
	let val = document.querySelector("#balance")
	fetch("http://localhost:5000/api/expenses")
	.then(body=>body.json())
	.then((x)=>{
		let node = document.querySelector(".transfer-section")
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
	fetch("http://localhost:5000/api/balance")
	.then(body=>body.json())
	.then((x)=>{
		form_data.append("amount", +(x.balance)-form.querySelector("input[name='amount']").value)
		fetch("http://localhost:5000/api/expenses", {
			method: "POST",
			body: form_data
		})
			.then(body=>body.json())
			.then((x)=>{
				if (!x.Success){
					alert(x.msg);
					main();
				} else {
					window.location = "http://localhost:5000/dashboard"
				}
			})
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
	fetch("http://localhost:5000/api/session",{
		method: "DELETE"
	})
	.then(()=>{
		window.location = "http://localhost:5000/"
	})
}


const data = {
	labels: [
		"Food",
		"Entertainment",
		"Shopping",
		"EMI",
		"Rent",
		"Others"
	],
	datasets: [{
		label: 'Expenses',
		data: [0,0,0,0,0,0],
		fill: true,
		backgroundColor: 'rgba(255, 99, 132, 0.2)',
		borderColor: 'rgb(255, 99, 132)',
		pointBackgroundColor: 'rgb(255, 99, 132)',
		pointBorderColor: '#fff',
		pointHoverBackgroundColor: '#fff',
		pointHoverBorderColor: 'rgb(255, 99, 132)'
	}]
};

const config = {
	type: 'radar',
	data: data,
	options: {
		elements: {
			line: {
				borderWidth: 3
			}
		},
		scale: {
			min: 0
		},
	},
};

const loadGraph = () => {
	fetch("http://localhost:5000/api/expenses_by_category")
	.then(body=>body.json())
	.then((x)=>{
		console.log(x);
		config.data.datasets[0].data = [x.food, x.entertainment, x.shopping, x.emi, x.rent, x.others]
		window.myRadar = new Chart(document.getElementById("canvas"), config);
	})
};

const main = () => {
	displayBalance()
	displayName()
	loadGraph()
}

window.onload = main;

main();
