# Japanese sentences JP1K TSC note type.

Based on Japanese sentences types by Tatsumoto, nbelikov, Cyphar and the JP1K note types. 
This type can be used to follow the JP1K method of first thinking about the reading, revealing it and grading yourself based on meaning alone. (The readings are hidden and revealed on mouse hover or pressing P so this feature is optional). It's suitable for Sentence cards and Vocab cards (Vocab cards are shown when there is no `SentKanji` / `SentFurigana`), and it hides bilingual definitions when there's also a monolingual one.
I mixed these features and did some visual changes to day and night mode to go easy on the eyes since sometimes too much kanji on the screen can be a bit agressive. Color overall is less contrasting.

Use this note type if you:
  * Want to mine from subbed videos using mpvacious and Yomichan.
  * Want to improve the layout of your Sentence card collection (e.g. your own mined, Ankidrone Starter Pack, Kanji Transition, audio cards, subs2srs collections and Immersion Kit cards).
  * Want to migrate your old Word Context Card collection or your Sentence card collection to Targeted Sentence Cards.


## What's different? (compared to original note type)

Fields removed: `MorphManFocus`, `VocabPitchNum` (removed by nb)
Fields added: `VocabDefMono`, `Source` (added by Cyphar), I added `Hint`

  * I don't use MorphMan but you can add the needed field and it will work fine. I find Pitch accent coloration and numbering scheme not that useful when you have a graph and `VocabAudio`.
  * The Translate link didn't work anymore so I changed the site to DeepL and the Image link sends you to DuckDuckGo and only uses the VocabKanji field. It used to search for the whole sentence which showed inaccurate results.
  * Furigana is shown for the whole sentence when hovered, not just the hovered word.
  * Added the `Hint` field which is always shown. SentFurigana is prioritized on front just like JP1K so adding a hint furigana to `SentKanji` can't be used, I found best not to mess with it and use the `Hint` field instead. This field is also to ease the transition for people who are migrating from Word Context Cards that use hints and don't want to lose that info. If you're coming from WCC, when changing to sentence cards you'll notice that a lot of the hints are just extensions of the sentence but there are other ways of using this field that work with sentence cards like warning about repeatedly wrong readings or meanings.
  * The bolded words in the sentence are not only colored but also made a little bit bigger for a better grip on the sight. Also implemented bolded and colored words in the `VocabDef` and `VocabDefMono` for when sometimes there's more than one definition but want to highlight the one that fits the context. Although I think these should be filled minimally, there are times when you will find useful details about a word and want to keep that info to help your study.
  * Took from Cyphar the idea of hiding `VocabDef` as a hint when there's a monolingual definition. This is to help commit to the monolingual definitions, I found that if I had both, my eyes would automatically go for the latin script. If you don't want to use this feature you can have any definition on `VocabDef` and it will display as usual as long as `VocabDefMono` is empty.
  * There was a tag separation problem that is now fixed. Also changed the hand pointer of the tags because it made it seem as if they linked to somewhere.
  * Furigana made unselectable so you can copy the vocab or sentence cleanly. (this works on Windows Anki but not on Ankidroid, don't know why)
  * There are several {{edit:____}} tagged fields that work with the Edit Field During Review Cloze so you can edit them using Ctrl+click. (Though you should know that making `SentFurigana` and `VocabFurigana` editable fields will make this not work unless you Right click->Copy, so I left them not editable). Note that when an editable field is conditioned to not appear, the editable empty space is also gone so you have to use the Editor.
  * Fixed the image columns when there are several images.
  * Production cards are basically left the same. Did the same links fix like in the back of recognition cards.
  * Broke apart the Night Mode section in the CSS template as it made my editing easier. I put the parts bellow their corresponding Day Mode counterparts.
  * Please mind that Production cards only work when there's a 1)Vocab field present, 2)has furigana generated and 3)the `MakeProductionCard` field is not empty. Best to use it with Vocab+Sentence notes but also admits only Vocab notes.


## Screenshots

Below are the screenshots of *Recognition* cards.  *Production* cards are not
much different.

![Night front](https://raw.githubusercontent.com/Alksindrs/AnkiNoteTypes/main/templates/Japanese%20JP1K%20TSC/night%20front.webp)<br/>
*The front of the card showing the `Hint` field*

![Night back](/Japanese JP1K TSC/night back.webp?raw=true)<br/>
*Bilingual definition hidden and a bolded word on monolingual definition.*

![Day front](/Japanese JP1K TSC/day front.webp?raw=true)<br/>
*Day mode*

![Day back](/Japanese JP1K TSC/day back.webp?raw=true)<br/>
*`VocabDef` shown after pressing button.*


## Configuration

Most of the instructions for *Japanese sentences* template apply here as well,
with few changes.


### *Yomichan* settings

| Field           | Value                                             |
| --------------- | ------------------------------------------------- |
| `SentKanji`     | `{cloze-prefix}<b>{cloze-body}</b>{cloze-suffix}` |
| `VocabKanji`    | `{expression}`                                    |
| `VocabFurigana` | `{furigana-plain}`                                |
| `VocabDef`      | `{glossary-brief}`                                |
| `VocabAudio`    | `{audio}`                                         |


### Enable filling the Source field on *mpvacious* settings

In `subs2srs.conf` of miscinfo is mapped to Notes by default, make sure to change it to Source:

    miscinfo_enable=yes
    miscinfo_field=Source


## To be used with the following Anki addons

AJT Furigana 
AJT Pitch Accent
anki-forvo-dl
Edit Field During Review (Cloze)

And mpvacious or similar mpv scripts that work with Yomichan and AnkiConnect.
