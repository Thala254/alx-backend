import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';
import express from 'express';

const client = createClient();

const reserveSeat = async (number) => promisify(client.set).bind(client)('available_seats', number);

const getCurrentAvailableSeats = async () => promisify(client.get).bind(client)('available_seats');

const resetSeats = async () => promisify(client.set).bind(client)('available_seats', 50);

let reservationEnabled = true;

const queue = createQueue();
const app = express();

app.get('/available_seats', async (_, res) => res.json({ numberOfAvailableSeats: await getCurrentAvailableSeats() }));

app.get('/reserve_seat', (_, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  try {
    const job = queue.create('reserve_seat');
    job
      .on('failed', (err) => console.log(`Seat reservation job ${job.id} failed: ${err.message || err.toString()}`))
      .on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
    job.save();
    res.json({ status: 'Reservation in progress' });
  } catch (err) {
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', (_, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (_job, done) => {
    const seats = parseInt(await getCurrentAvailableSeats(), 10);
    reservationEnabled = seats === 0 ? false : reservationEnabled;
    if (seats >= 1) {
      await reserveSeat(seats - 1);
      done();
    }
    done(new Error('Not enough seats available'));
  });
});

app.listen(1245, async () => {
  await resetSeats();
  console.log('Server connected at port 1245');
});

export default app;
