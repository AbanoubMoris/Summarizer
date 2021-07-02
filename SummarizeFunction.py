from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config, AutoTokenizer, AutoModelWithLMHead, \
    AutoModelForSeq2SeqLM
import torch
import wordcounter
from wordcounter.wordcounter import WordCounter


def Summarize(document, summarization_rate):
    # tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    # model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-summarize-news")
    #
    # input_ids = tokenizer.encode(document, return_tensors="pt")
    # generated_ids = model.generate(input_ids=input_ids, num_beams=4, min_length=80, max_length=150, repetition_penalty=5.5,
    #                                early_stopping=False, no_repeat_ngram_size=2, length_penalty=0.6)
    # preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
    # return preds[0]


    # Old Method
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')
    preprocess_text = document.strip().replace("\n", " ")
    t5_prepared_Text = "summarize: " + preprocess_text
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt", max_length=5000, truncation=True).to(
        device)

    word_counter = WordCounter(document, delimiter=' ')
    doc_len = word_counter.get_word_count()
    rate = int(doc_len * (summarization_rate/100))
    summary_ids = model.generate(tokenized_text,
                                 num_beams=2,
                                 no_repeat_ngram_size=2,
                                 min_length=rate,
                                 max_length=doc_len,
                                 early_stopping=False)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output