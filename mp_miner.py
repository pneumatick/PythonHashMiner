import sys
import hashlib
from rehash import sha256
import multiprocessing as mp
import pickle

# Add the nonce to the context, and add the data + nonce to the queue if it
# the resulting hash starts with the target. The process will repeat until
# 32 bits are exhausted.
# NOTE: Striping is used to achieve greater efficiency (hence the final line).
def work(context, i, data, target, queue, num_workers):
    while i < 2 ** 32:
        nonced_hash = pickle.loads(context)
        nonced_hash.update(str(i).encode())
        if nonced_hash.hexdigest()[:len(target)] == target:
            queue.put(data + str(i))
        i += num_workers

if __name__ == '__main__':
    data = sys.argv[1]
    target = sys.argv[2]
    context = pickle.dumps(sha256(data.encode()))
    queue = mp.Queue()
    num_workers = mp.cpu_count()
    process_list = []

    # Execute each process.
    for i in range(num_workers):
        p = mp.Process(target=work,
                       args=(context, i, data, target, queue, num_workers))
        p.start()
        process_list.append(p)

    # Loop until the user quits (via ctrl-c)
    while True:
        try:
            output = queue.get(block = True, timeout = 1.0)
            if output:
                # Print data
                print("Data (with nonce): " + output)
                print("Hash: " + hashlib.sha256(output.encode()).hexdigest())
        except KeyboardInterrupt:
            print("User cancelled.")
            break
        except Exception as e:
            pass
    queue.close()

    # Terminate each process.
    for p in process_list:
        p.terminate()
