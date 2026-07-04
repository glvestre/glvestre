# Google Flow — Guide complet de prompting (Veo 3 / Veo 3.1)

> Base de connaissances compilée le 2026-07-04 à partir de la documentation officielle Google (DeepMind, Google Cloud, Google Labs) et de guides de créateurs viraux. Sources complètes dans `03-sources.md`.

---

## 1. Qu'est-ce que Google Flow ?

**Flow** (labs.google/flow) est l'outil de "AI filmmaking" de Google, conçu pour le modèle vidéo **Veo**. Lancé au Google I/O en mai 2025, propulsé par **Veo 3** puis **Veo 3.1** (octobre 2025).

### Chiffres clés
- **100 millions de vidéos** générées en 90 jours (annonce Demis Hassabis, 19 août 2025)
- **275 millions de vidéos** en 5 premiers mois
- ~**1,1 million de vidéos générées par jour**
- Disponible dans **149+ pays** via les abonnements Google AI Pro, AI Ultra et AI Ultra for Business
- Plan Ultra (~250 $/mois) : jusqu'à 25 000 crédits par cycle — le plan utilisé par les créateurs viraux à gros volume

### Modes de génération
| Mode | Description |
|------|-------------|
| **Text to Video** | Prompt texte → clip vidéo avec audio natif (dialogues, SFX, musique) |
| **Frames to Video** | Image(s) de départ (et de fin) → vidéo animée entre les deux |
| **Ingredients to Video** | Jusqu'à 3 images de référence (personnage, objet, décor) → cohérence visuelle entre les clips |

### Fonctionnalités d'édition
- **SceneBuilder** : timeline pour arranger, couper, réordonner les clips ; étendre un plan ou enchaîner sur l'action suivante avec mouvement continu et personnages cohérents
- **Extend** : rallonger un clip existant en décrivant la suite de l'action
- **Camera Controls** : contrôle direct du mouvement caméra (dolly in, pan left, etc.), angles et perspectives
- **Add/Remove Object** (Veo 3.1) : ajouter/retirer un objet en préservant la composition

### Caractéristiques techniques (Veo 3.1)
- Résolution : **720p ou 1080p**
- Formats : **16:9 et 9:16** (le vertical natif = essentiel pour TikTok/Reels/Shorts)
- Durée des clips : **4, 6 ou 8 secondes**
- **Audio natif synchronisé** : dialogues multi-personnages, bruitages, ambiances, musique
- Watermark invisible **SynthID** sur toutes les vidéos

---

## 2. La formule de prompt officielle (Google Cloud)

```
[Cinématographie] + [Sujet] + [Action] + [Contexte] + [Style & Ambiance]
```

| Élément | Définition | Exemples |
|---------|------------|----------|
| **Cinématographie** | Travail de caméra et composition du plan | Medium shot, crane shot, tracking shot, close-up, wide-angle lens, shallow depth of field |
| **Sujet** | Personnage ou point focal principal | "a tired corporate worker", "a female pop star", "a young female explorer" |
| **Action** | Ce que fait le sujet | "rubbing his temples in exhaustion", "singing passionately" |
| **Contexte** | Environnement et arrière-plan | "in front of a bulky 1980s computer in a cluttered office" |
| **Style & Ambiance** | Esthétique, humeur, lumière | "Retro aesthetic, shot as if on 1980s color film, slightly grainy", "cinematic", "moody with cool blue tones" |

> Conseil officiel : **commencer par la cinématographie** — c'est le levier le plus puissant pour le ton et l'émotion.

### Vocabulaire caméra essentiel

**Mouvements** : dolly shot, tracking shot, crane shot, aerial view, slow pan, POV shot, 180-degree arc shot

**Composition** : wide shot, medium shot, close-up, extreme close-up, low angle, high-angle crane shot, two-shot, reverse shot

**Objectif & focus** : shallow depth of field, wide-angle lens, soft focus, macro lens, deep focus

---

## 3. Direction audio (la killer feature de Veo 3)

### Dialogue — syntaxe avec guillemets
```
A woman says, "We have to leave now."
He looks up and says in a weary voice, "Of all the offices in this town, you had to walk into mine."
```

### Effets sonores (SFX)
```
SFX: thunder cracks in the distance
SFX: The rustle of dense leaves, distant exotic bird calls
```

### Ambiance sonore
```
Ambient noise: the quiet hum of a starship bridge
```

### ⚠️ Astuce anti-sous-titres
Ajouter **"no subtitles"** (ou "no on-screen text") dans le prompt — erreur n°1 des débutants, confirmée par les créateurs viraux (le créateur du Bigfoot POV viral l'avait oublié dans sa première version).

---

## 4. Negative prompting

Utiliser des **exclusions spécifiques** plutôt que des négations génériques :
- ✅ "a desolate landscape with no buildings or roads"
- ❌ "no man-made structures"

---

## 5. Timestamp prompting (séquence multi-plans en 1 génération)

```
[00:00-00:02] Medium shot from behind a young female explorer with a leather
satchel, as she pushes aside a large jungle vine to reveal a hidden path.

[00:02-00:04] Reverse shot of the explorer's freckled face, filled with awe as
she gazes upon ancient moss-covered ruins. SFX: rustle of leaves, distant bird calls.

[00:04-00:06] Tracking shot following the explorer as she runs her hand over
the carvings on a crumbling stone wall. Emotion: wonder and reverence.

[00:06-00:08] Wide, high-angle crane shot revealing the lone explorer standing
small in the vast forgotten temple complex. SFX: a swelling orchestral score begins.
```

---

## 6. Workflows avancés Veo 3.1 dans Flow

### Workflow A — Transition "First & Last Frame"
1. Générer l'image de départ (Gemini 2.5 Flash Image) : *"Medium shot of a female pop star singing into a vintage microphone, dark stage, single dramatic spotlight…"*
2. Générer l'image de fin : *"POV shot from behind the singer looking out at a cheering crowd…"*
3. Animer avec Veo 3.1 : *"The camera performs a smooth 180-degree arc shot… The singer sings 'when you look me in the eyes, I can see a million stars.'"*

### Workflow B — Scène dialoguée avec "Ingredients to Video"
1. Générer des images de référence : personnage A, personnage B, décor
2. Plan 1 : *"Using the provided images for the detective, the woman, and the office setting, create a medium shot of the detective behind his desk. He says in a weary voice, '…'"*
3. Plan 2 : même formule en changeant le focus → **cohérence des personnages entre les plans**

---

## 7. JSON prompting (technique virale de précision)

Structurer le prompt en paires clé-valeur → **consistance nettement supérieure** aux prompts texte pour les séries de vidéos (les créateurs viraux l'utilisent pour garder un personnage identique sur 50+ vidéos).

```json
{
  "shot": {
    "type": "selfie POV, handheld",
    "lens": "wide-angle, slight distortion",
    "camera_motion": "shaky, walking pace"
  },
  "subject": {
    "character": "a friendly yeti with matted white fur and blue eyes",
    "action": "vlogging while hiking through a snowstorm"
  },
  "scene": {
    "location": "himalayan ridge at dusk",
    "weather": "heavy snow, wind"
  },
  "audio": {
    "dialogue": "Day 47. Still no sign of the film crew. Honestly? Thriving.",
    "sfx": "howling wind, crunching snow",
    "ambient": "distant avalanche rumble"
  },
  "style": {
    "aesthetic": "hyper-realistic vlog footage, 4k",
    "no_subtitles": true
  }
}
```

---

## 8. Le template "vlog viral" (formule des créateurs)

Formule popularisée par Synthesia/les créateurs stormtrooper (des millions de vues sur TikTok) :

```
A stormtrooper is {Action} in {Location}. He is holding his camera in vlog
selfie-cam style and says "{Script}"
```

Exemple :
```
A stormtrooper walking fast in a snowy area with another stormtrooper beside him.
In the distance, Darth Vader follows them. He is holding his camera in vlog
selfie-cam style and says "We made it out of Vader's ship in one piece.
Seriously, that guy is the worst boss ever."
```

### Prompt viral complet réel — "Jonas dans la baleine" (PJ Ace, @pjacefilms, des millions de vues)

```
A cinematic handheld selfie-style video shot, showing a soggy, exhausted Middle
Eastern man in his 30s with shoulder-length wet hair, a tangled beard, and
shredded linen robes clinging to his frame. He's seated awkwardly on a slick,
uneven surface deep inside the belly of a massive sea creature. The fleshy,
ribbed walls pulse slightly around him, dimly lit by a faint blue-green glow
coming from slits in the whale's tissue above. Water drips steadily in the
background. He holds the camera close, his face lit softly by the glow, his
expression weary and mildly guilty. He talks with a country accent.

He says: "Update, still swallowed. I would like to formally apologize to God,
the sailors, and this whale, sorry dude, I just took a poop over there."

He glances offscreen and winces slightly, then gives the camera a sheepish
shrug before shifting uncomfortably.
Time of Day: indeterminate interior, faint bioluminescent glow from above
Lens: natural wide framing, dim exposure optimized for low light and moisture
POV: Selfie camera held close to face, angled upward slightly
Audio: (implied) dripping water, faint groaning of the whale's body, distant
liquid movement
Background: wet, fleshy whale interior with ribbed walls and dim, humid atmosphere
```

### Workflow des pros (PJ Ace — pub Kalshi, vlogs bibliques)
1. **Script de base avec ChatGPT** (ou Gemini/Grok)
2. **Expansion en shot list** avec la structure de prompt ci-dessus
3. **Coller dans Veo 3 / Flow** et générer plusieurs variantes, garder les meilleures
4. **Montage** dans Final Cut / CapCut

---

## 9. Bonnes pratiques (synthèse)

1. Utiliser la formule en 5 parties, cinématographie en premier
2. Guillemets pour les dialogues, `SFX:` pour les bruitages, `Ambient noise:` pour l'ambiance
3. **Toujours "no subtitles"** pour les vlogs
4. Exclusions spécifiques, pas de négations génériques
5. Gemini 2.5 Flash Image pour générer les images de référence (cohérence personnages)
6. Timestamp prompting pour les séquences multi-plans
7. JSON prompting pour les personnages récurrents / séries
8. Compter **5-10 générations par clip utilisable** (Kalshi : 15 clips retenus sur ~400 générations)
9. Coût réel estimé : ~3 $/clip en plan Ultra → ~100 $/vidéo de 60 s avec les ratés
10. Format 9:16 natif pour TikTok / Reels / Shorts
