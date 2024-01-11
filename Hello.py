# app.py
from dotenv import load_dotenv, find_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
import streamlit as st
import os
os.environ['OPENAI_API_KEY'] = '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'

def init_page():
    st.set_page_config(
        page_title="Личный ChatGPT"
    )
    st.header("Личный ChatGPT")
    st.sidebar.title("Опции")


def init_messages():
    clear_button = st.sidebar.button("Очистить Беседу", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content="Вы - полезный AI ассистент. Отвечайте на вопросы в формате markdown.")
        ]
        st.session_state.costs = []


def select_model():
    model_name = st.sidebar.radio("Выберите LLM:",
                                  ("gpt-3.5-turbo-0613", "gpt-4"))
    temperature = st.sidebar.slider("Температура:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    return ChatOpenAI(temperature=temperature, model_name=model_name)


def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost


def main():
    _ = load_dotenv(find_dotenv())

    init_page()
    llm = select_model()
    init_messages()

    # Проверка ввода пользователя
    if user_input := st.chat_input("Введите ваш вопрос!"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT печатает ..."):
            answer, cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer))
        st.session_state.costs.append(cost)

    # Показ истории чата
    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

    costs = st.session_state.get("costs", [])
    st.sidebar.markdown("## Стоимость")
    st.sidebar.markdown(f"**Общая стоимость: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


if __name__ == "__main__":
    main()
