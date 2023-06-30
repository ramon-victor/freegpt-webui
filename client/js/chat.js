const query = (obj) =>
  Object.keys(obj)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
    .join("&");
const markdown = window.markdownit();
const message_box = document.getElementById(`messages`);
const message_input = document.getElementById(`message-input`);
const box_conversations = document.querySelector(`.top`);
const spinner = box_conversations.querySelector(".spinner");
const stop_generating = document.querySelector(`.stop-generating`);
const send_button = document.querySelector(`#send-button`);
const user_image = `<img src="/assets/img/user.png" alt="User Avatar">`;
const gpt_image = `<img src="/assets/img/gpt.png" alt="GPT Avatar">`;
let prompt_lock = false;

hljs.addPlugin(new CopyButtonPlugin());

message_input.addEventListener("blur", () => {
  window.scrollTo(0, 0);
});

message_input.addEventListener("focus", () => {
  document.documentElement.scrollTop = document.documentElement.scrollHeight;
});

const delete_conversations = async () => {
  localStorage.clear();
  await new_conversation();
};

const handle_ask = async () => {
  message_input.style.height = `80px`;
  window.scrollTo(0, 0);
  let message = message_input.value;

  if (message.length > 0) {
    message_input.value = ``;
    message_input.dispatchEvent(new Event("input"));
    await ask_gpt(message);
  }
};

const remove_cancel_button = async () => {
  stop_generating.classList.add(`stop-generating-hiding`);

  setTimeout(() => {
    stop_generating.classList.remove(`stop-generating-hiding`);
    stop_generating.classList.add(`stop-generating-hidden`);
  }, 300);
};

const ask_gpt = async (message) => {
  try {
    message_input.value = ``;
    message_input.innerHTML = ``;
    message_input.innerText = ``;

    add_conversation(window.conversation_id, message.substr(0, 20));
    window.scrollTo(0, 0);
    window.controller = new AbortController();

    jailbreak = document.getElementById("jailbreak");
    model = document.getElementById("model");
    prompt_lock = true;
    window.text = ``;
    window.token = message_id();

    stop_generating.classList.remove(`stop-generating-hidden`);

    add_user_message_box(message);

    message_box.scrollTop = message_box.scrollHeight;
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 500));
    window.scrollTo(0, 0);

    message_box.innerHTML += `
            <div class="message">
                <div class="avatar-container">
                    ${gpt_image}
                </div>
                <div class="content" id="gpt_${window.token}">
                    <div id="cursor"></div>
                </div>
            </div>
        `;

    message_box.scrollTop = message_box.scrollHeight;
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 1000));
    window.scrollTo(0, 0);

    const response = await fetch(`/backend-api/v2/conversation`, {
      method: `POST`,
      signal: window.controller.signal,
      headers: {
        "content-type": `application/json`,
        accept: `text/event-stream`,
      },
      body: JSON.stringify({
        conversation_id: window.conversation_id,
        action: `_ask`,
        model: model.options[model.selectedIndex].value,
        jailbreak: jailbreak.options[jailbreak.selectedIndex].value,
        meta: {
          id: window.token,
          content: {
            conversation: await get_conversation(window.conversation_id),
            internet_access: document.getElementById("switch").checked,
            content_type: "text",
            parts: [
              {
                content: message,
                role: "user",
              },
            ],
          },
        },
      }),
    });

    const reader = response.body.getReader();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      chunk = decodeUnicode(new TextDecoder().decode(value));

      if (
        chunk.includes(
          `<form id="challenge-form" action="/backend-api/v2/conversation?`
        )
      ) {
        chunk = `cloudflare token expired, please refresh the page.`;
      }

      text += chunk;

      document.getElementById(`gpt_${window.token}`).innerHTML =
        markdown.render(text);
      document.querySelectorAll(`code`).forEach((el) => {
        hljs.highlightElement(el);
      });

      window.scrollTo(0, 0);
      message_box.scrollTo({ top: message_box.scrollHeight, behavior: "auto" });
    }

    // if text contains :
    if (
      text.includes(
        `instead. Maintaining this website and API costs a lot of money`
      )
    ) {
      document.getElementById(`gpt_${window.token}`).innerHTML =
        "An error occurred, please reload / refresh cache and try again.";
    }

    add_message(window.conversation_id, "user", message);
    add_message(window.conversation_id, "assistant", text);

    message_box.scrollTop = message_box.scrollHeight;
    await remove_cancel_button();
    prompt_lock = false;

    await load_conversations(20, 0);
    window.scrollTo(0, 0);
  } catch (e) {
    add_message(window.conversation_id, "user", message);

    message_box.scrollTop = message_box.scrollHeight;
    await remove_cancel_button();
    prompt_lock = false;

    await load_conversations(20, 0);

    console.log(e);

    let cursorDiv = document.getElementById(`cursor`);
    if (cursorDiv) cursorDiv.parentNode.removeChild(cursorDiv);

    if (e.name != `AbortError`) {
      let error_message = `oops ! something went wrong, please try again / reload. [stacktrace in console]`;

      document.getElementById(`gpt_${window.token}`).innerHTML = error_message;
      add_message(window.conversation_id, "assistant", error_message);
    } else {
      document.getElementById(`gpt_${window.token}`).innerHTML += ` [aborted]`;
      add_message(window.conversation_id, "assistant", text + ` [aborted]`);
    }

    window.scrollTo(0, 0);
  }
};

const add_user_message_box = (message) => {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");

  const avatarContainer = document.createElement("div");
  avatarContainer.classList.add("avatar-container");
  avatarContainer.innerHTML = user_image;

  const contentDiv = document.createElement("div");
  contentDiv.classList.add("content");
  contentDiv.id = `user_${token}`;
  contentDiv.innerText = message;

  messageDiv.appendChild(avatarContainer);
  messageDiv.appendChild(contentDiv);

  message_box.appendChild(messageDiv);
};

const decodeUnicode = (str) => {
  return str.replace(/\\u([a-fA-F0-9]{4})/g, function (match, grp) {
    return String.fromCharCode(parseInt(grp, 16));
  });
};

const clear_conversations = async () => {
  const elements = box_conversations.childNodes;
  let index = elements.length;

  if (index > 0) {
    while (index--) {
      const element = elements[index];
      if (
        element.nodeType === Node.ELEMENT_NODE &&
        element.tagName.toLowerCase() !== `button`
      ) {
        box_conversations.removeChild(element);
      }
    }
  }
};

const clear_conversation = async () => {
  let messages = message_box.getElementsByTagName(`div`);

  while (messages.length > 0) {
    message_box.removeChild(messages[0]);
  }
};

const delete_conversation = async (conversation_id) => {
  localStorage.removeItem(`conversation:${conversation_id}`);

  if (window.conversation_id == conversation_id) {
    await new_conversation();
  }

  await load_conversations(20, 0, true);
};

const set_conversation = async (conversation_id) => {
  history.pushState({}, null, `/chat/${conversation_id}`);
  window.conversation_id = conversation_id;

  await clear_conversation();
  await load_conversation(conversation_id);
  await load_conversations(20, 0, true);
};

const new_conversation = async () => {
  history.pushState({}, null, `/chat/`);
  window.conversation_id = uuid();

  await clear_conversation();
  await load_conversations(20, 0, true);
};

const load_conversation = async (conversation_id) => {
  let conversation = await JSON.parse(
    localStorage.getItem(`conversation:${conversation_id}`)
  );

  for (item of conversation.items) {
    if (is_assistant(item.role)) {
      message_box.innerHTML += load_gpt_message_box(item.content);
    } else {
      message_box.innerHTML += load_user_message_box(item.content);
    }
  }

  document.querySelectorAll(`code`).forEach((el) => {
    hljs.highlightElement(el);
  });

  message_box.scrollTo({ top: message_box.scrollHeight, behavior: "smooth" });

  setTimeout(() => {
    message_box.scrollTop = message_box.scrollHeight;
  }, 500);
};

const load_user_message_box = (content) => {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");

  const avatarContainer = document.createElement("div");
  avatarContainer.classList.add("avatar-container");
  avatarContainer.innerHTML = user_image;

  const contentDiv = document.createElement("div");
  contentDiv.classList.add("content");
  contentDiv.innerText = content;

  messageDiv.appendChild(avatarContainer);
  messageDiv.appendChild(contentDiv);

  return messageDiv.outerHTML;
};

const load_gpt_message_box = (content) => {
  return `
            <div class="message">
                <div class="avatar-container">
                    ${gpt_image}
                </div>
                <div class="content">
                    ${markdown.render(content)}
                </div>
            </div>
        `;
};

const is_assistant = (role) => {
  return role == "assistant";
};

const get_conversation = async (conversation_id) => {
  let conversation = await JSON.parse(
    localStorage.getItem(`conversation:${conversation_id}`)
  );
  return conversation.items;
};

const add_conversation = async (conversation_id, title) => {
  if (localStorage.getItem(`conversation:${conversation_id}`) == null) {
    localStorage.setItem(
      `conversation:${conversation_id}`,
      JSON.stringify({
        id: conversation_id,
        title: title,
        items: [],
      })
    );
  }
};

const add_message = async (conversation_id, role, content) => {
  before_adding = JSON.parse(
    localStorage.getItem(`conversation:${conversation_id}`)
  );

  before_adding.items.push({
    role: role,
    content: content,
  });

  localStorage.setItem(
    `conversation:${conversation_id}`,
    JSON.stringify(before_adding)
  ); // update conversation
};

const load_conversations = async (limit, offset, loader) => {
  let conversations = [];
  for (let i = 0; i < localStorage.length; i++) {
    if (localStorage.key(i).startsWith("conversation:")) {
      let conversation = localStorage.getItem(localStorage.key(i));
      conversations.push(JSON.parse(conversation));
    }
  }

  await clear_conversations();

  for (conversation of conversations) {
    box_conversations.innerHTML += `
            <div class="conversation-sidebar">
                <div class="left" onclick="set_conversation('${conversation.id}')">
                    <i class="fa-regular fa-comments"></i>
                    <span class="conversation-title">${conversation.title}</span>
                </div>
                <i onclick="delete_conversation('${conversation.id}')" class="fa-regular fa-trash"></i>
            </div>
        `;
  }

  document.querySelectorAll(`code`).forEach((el) => {
    hljs.highlightElement(el);
  });
};

document.getElementById(`cancelButton`).addEventListener(`click`, async () => {
  window.controller.abort();
});

function h2a(str1) {
  var hex = str1.toString();
  var str = "";

  for (var n = 0; n < hex.length; n += 2) {
    str += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
  }

  return str;
}

const uuid = () => {
  return `xxxxxxxx-xxxx-4xxx-yxxx-${Date.now().toString(16)}`.replace(
    /[xy]/g,
    function (c) {
      var r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    }
  );
};

const message_id = () => {
  random_bytes = (Math.floor(Math.random() * 1338377565) + 2956589730).toString(
    2
  );
  unix = Math.floor(Date.now() / 1000).toString(2);

  return BigInt(`0b${unix}${random_bytes}`).toString();
};

window.onload = async () => {
  load_settings_localstorage();

  conversations = 0;
  for (let i = 0; i < localStorage.length; i++) {
    if (localStorage.key(i).startsWith("conversation:")) {
      conversations += 1;
    }
  }

  if (conversations == 0) localStorage.clear();

  await setTimeout(() => {
    load_conversations(20, 0);
  }, 1);

  if (!window.location.href.endsWith(`#`)) {
    if (/\/chat\/.+/.test(window.location.href)) {
      await load_conversation(window.conversation_id);
    }
  }

  message_input.addEventListener("keydown", async (evt) => {
    if (prompt_lock) return;

    if (evt.key === "Enter" && !evt.shiftKey) {
      evt.preventDefault();
      await handle_ask();
    }
  });

  send_button.addEventListener("click", async (event) => {
    event.preventDefault();
    if (prompt_lock) return;
    message_input.blur();
    await handle_ask();
  });

  register_settings_localstorage();
};

document.querySelector(".mobile-sidebar").addEventListener("click", (event) => {
  const sidebar = document.querySelector(".sidebar");

  if (sidebar.classList.contains("shown")) {
    sidebar.classList.remove("shown");
    event.target.classList.remove("rotated");
    document.body.style.overflow = "auto";
  } else {
    sidebar.classList.add("shown");
    event.target.classList.add("rotated");
    document.body.style.overflow = "hidden";
  }

  window.scrollTo(0, 0);
});

const register_settings_localstorage = async () => {
  settings_ids = ["switch", "model", "jailbreak"];
  settings_elements = settings_ids.map((id) => document.getElementById(id));
  settings_elements.map((element) =>
    element.addEventListener(`change`, async (event) => {
      switch (event.target.type) {
        case "checkbox":
          localStorage.setItem(event.target.id, event.target.checked);
          break;
        case "select-one":
          localStorage.setItem(event.target.id, event.target.selectedIndex);
          break;
        default:
          console.warn("Unresolved element type");
      }
    })
  );
};

const load_settings_localstorage = async () => {
  settings_ids = ["switch", "model", "jailbreak"];
  settings_elements = settings_ids.map((id) => document.getElementById(id));
  settings_elements.map((element) => {
    if (localStorage.getItem(element.id)) {
      switch (element.type) {
        case "checkbox":
          element.checked = localStorage.getItem(element.id) === "true";
          break;
        case "select-one":
          element.selectedIndex = parseInt(localStorage.getItem(element.id));
          break;
        default:
          console.warn("Unresolved element type");
      }
    }
  });
};

function clearTextarea(textarea) {
  textarea.style.removeProperty("height");
  textarea.style.height = `${textarea.scrollHeight + 4}px`;

  if (textarea.value.trim() === "" && textarea.value.includes("\n")) {
    textarea.value = "";
  }
}
