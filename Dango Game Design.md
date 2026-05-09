**Dango Shop**

Game Design Document  
**Items in PINK are Considered MVP**

# **1\. Overview**

Dango Shop is a 2D action game set in a traditional Japanese sweet shop. The player controls a character hovering in the shop, catching dango balls fired from a rotating cannon and assembling them onto a skewer to fill customer orders. Balls come in different flavours with distinct flight behaviours. Customers queue up with orders and grow impatient if kept waiting too long.

# **2\. Core Loop**

* The cannon fires a volley of dango balls sized to the current stick capacity.

* The player catches desired balls, parries unwanted balls up to the priority queue or down to the hopper bag.

* Once the order is made, the player serves it. The order is matched against waiting customers.

* Matched orders pay yen. Unmatched orders go to the 10-slot display stand for passing customers to claim.

* Dango balls that hit the player or reach the backstop each incur a −50¥ penalty.

* Customers who are not served in time leave, also incurring a −50¥ penalty.

* Each day has a yen quota. Fail to meet it, and the day fails.

# **3\. Controls**

| Action | Controller (Xbox) | Keyboard | Description |
| :---- | :---- | :---- | :---- |
| **Move** | Left Stick | W A S D | Move character |
| **Stab** | B | Space | Catch incoming dango ball onto stick |
| **Parry Up** | Y | H | Send ball to priority queue (jumps to front) |
| **Parry Down** | A | J | Send ball back to hopper bag (removes from play) |
| **Serve** | X | Enter | Serve completed stick to display stand |
| **Discard** | LB | Ctrl | Discard currently selected display stand slot (point penalty) |
| **Dash** | RB | Shift | Dash in movement direction; can combine with stab |
| **Pause** | (pause button) | P | Pause / unpause the game |

# **4\. Dango Balls**

## **4.1 Flight Patterns**

All balls bounce off the floor and ceiling. Each colour has a distinct flight pattern introduced on a specific day. The cannon rotates, changing the launch angle.

| Color | Flavor | Flight Pattern | Special Mechanic |
| :---- | :---- | :---- | :---- |
| **Pink** | Sakura / Red Bean | Straight, slow | X |
| **White** | Plain / Shiratama | Straight, fast | X |
| **Green** | Matcha | Sine wave (up/down) | X |
| **Yellow** | Egg / Custard | Gentle home toward player | Rewards lazy play; punishes unwanted catches |
| **Brown** | Mitarashi (Soy \+ Sugar) | Gentle home away from player | Must lead and predict trajectory |
| **Orange** | Chestnut | Decelerates mid-flight, re-accel. | Rhythm disruption; punishes early stab |
| **Purple** | Taro | Straight, medium | Proximity dodge \+ cloud visual; blink cooldown outline |
| **Black** | Black Sesame | Straight, medium | Shadow decoy on launch; rarest ball (1 copy per bag) |

## **4.2 Purple Ball Dodge Detail**

* Dodge triggers on proximity (stab range), not raw stab input.

* First approach triggers dodge; player can follow up immediately during cooldown to catch it.

* Cooldown is shown as a blinking outline on the ball.

* Leaves behind a small cloud.

## **4.3 Black Ball Shadow Decoy Detail**

* On launch, a shadow decoy is also fired on a slightly different path.

* The decoy looks similar to the real ball but not identical. Players learn to distinguish them.

* Stabbing the decoy misses; only the real ball can be caught.

# **5\. Hazards**

Hazards are drawn from the same bag as dango balls. Parrying a hazard (up or down) removes it from play entirely. Hazards hitting the backstop incur no penalty.

| Hazard | Appearance | Spawn | Effect on Catch |
| :---- | :---- | :---- | :---- |
| **Wasabi** | Bright green. Distinct from matcha | Straight, fast | Scrambles controls for 10s: all directions flipped, parry buttons swapped |
| **Hot Coal** | Glowing ember ball | Burst of 3 (shotgun) | Burns stick entirely on catch — all built-up dango lost |

# **6\. Queue & Hopper System**

## **6.1 Queue**

* The queue displays the next 10 \- 15 upcoming balls visually (bubble shooter style).

* Parry-up sends the ball to a priority feed — it jumps to the front of the queue.

* Parry-down sends the ball back to the hopper bag.

* The queue has no hard capacity limit that causes deadlocks — priority balls always cut the line.

## **6.2 Bag System**

Each day uses a fixed bag definition. The bag is shuffled and drawn from. When empty, a new, shuffled bag is generated. This prevents long colour droughts.

| Day | Bag Contents | Stick Size |
| :---- | :---- | :---- |
| **1** | Pink ×4, White ×4 | 2 |
| **2** | Pink ×4, White ×4, Green ×3 | 3 |
| **3** | Pink ×4, White ×4, Green ×3, Yellow ×2, Wasabi ×1 | 3 |
| **4** | Pink ×4, White ×4, Green ×3, Yellow ×2, Brown ×2, Wasabi ×1 | 4 |
| **5** | Pink ×4, White ×4, Green ×3, Yellow ×2, Brown ×2, Orange ×2, Wasabi ×1, Coal ×1 | 4 |
| **6** | Pink ×4, White ×4, Green ×3, Yellow ×2, Brown ×2, Orange ×2, Purple ×2, Wasabi ×1, Coal ×1 | 5 |
| **7** | Pink ×4, White ×4, Green ×3, Yellow ×2, Brown ×2, Orange ×2, Purple ×2, Black ×1, Wasabi ×1, Coal ×1 | 5 |

# 

# **7\. Customer System**

* Customers queue up and display their order in a thought bubble.

* Orders can be fulfilled in any order.

* Customers grow impatient over time and eventually leave, penalizing the player.

* Dango sticks with no demand are kept in the display stand till claimed. (10 Slots)

## **7.1 Flavour Demand Weights**

The flavour demand will make use of the same bag system as described above, with doubled bag sizes (all ball colour counts also doubled) to introduce more variance in orders.

# **8\. Scoring**

## **8.1 Serve Formula**

Each serve is worth: (sum of ball base values) \+ (10¥ × \#balls ^2).

| Color | Base Value |
| :---- | :---- |
| **Pink** | 50¥ |
| **White** | 50¥ |
| **Green** | 50¥ |
| **Yellow** | 100¥ |
| **Brown** | 100¥ |
| **Orange** | 150¥ |
| **Purple** | 150¥ |
| **Black** | 250¥ |

Ex: 3-ball stick of Pink \+ Yellow \+ Black \= (50 \+ 100 \+ 250\) \+ 10 × (3 ^ 2\) \= 400 \+ 90 \= 490¥.

## **8.2 Penalties**

| Event | Effect |
| :---- | :---- |
| **Matched serve** | Sum of ball values \+ 50¥ × stick length |
| **Ball hits player** | −50¥ per hit |
| **Ball hits backstop** | −50¥ per ball missed |
| **Customer leaves unserved** | −50¥ per customer |
| **Discard from stand slot** | −50¥ per ball discarded |

## **8.3 Daily Quotas**

Each day lasts approximately 2 minutes. Rounds end when the quota is met or the time runs out. From day 7 onward, the game continues indefinitely with the same bag and quota until the player fails to meet the threshold. 

| Day | Quota (To Be Adjusted) |
| :---- | :---- |
| **1** | **2,000¥** |
| **2** | **2,500¥** |
| **3** | **3,000¥** |
| **4** | **3,500¥** |
| **5** | **4,000¥** |
| **6** | **5,000¥** |
| **7+** | **5,500¥** |

## 

## 

