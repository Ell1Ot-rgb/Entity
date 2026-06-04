"""
CTM v5.0 Dataset Generator
Especialista: ctm-sakai-manager (@dkeekwwk.ctm_sakai)
Generador de datos sintéticos para entrenamiento del sistema CTM v5.0
"""

import numpy as np
import torch
import h5py
import pandas as pd
from typing import Tuple, Dict, List
import os

class CTMv5DatasetGenerator:
    """Generador de datasets sintéticos para CTM v5.0"""

    def __init__(self, seed=42):
        np.random.seed(seed)
        torch.manual_seed(seed)

    def generate_dual_vector_sequences(self, num_samples=1000, output_dir='./data'):
        """Genera el Dual Vector Sequences Dataset"""
        print(f"Generando {num_samples} muestras de DVSD...")

        os.makedirs(output_dir, exist_ok=True)

        # Generar vectores neuronales (simulando actividad SNN)
        vector_neuro = np.random.randn(num_samples, 256).astype(np.float32)
        vector_neuro = np.tanh(vector_neuro)  # Activaciones típicas de SNN

        # Generar vectores fenomenológicos (simulando métricas físicas)
        vector_phenom = np.random.randn(num_samples, 256).astype(np.float32)
        vector_phenom = np.abs(vector_phenom)  # Métricas físicas positivas

        # Generar etiquetas de sincronización
        sync_labels = np.random.uniform(0.0, 1.0, num_samples).astype(np.float32)
        timestamps = np.arange(num_samples, dtype=np.int64)

        # Guardar en formato HDF5
        with h5py.File(os.path.join(output_dir, 'dvsd_synthetic.h5'), 'w') as f:
            f.create_dataset('vector_neuro', data=vector_neuro)
            f.create_dataset('vector_phenom', data=vector_phenom)
            f.create_dataset('sync_label', data=sync_labels)
            f.create_dataset('timestamp', data=timestamps)

        print(f"✅ DVSD generado: {num_samples} muestras")
        return os.path.join(output_dir, 'dvsd_synthetic.h5')

    def generate_markovian_memory_tasks(self, num_episodes=1000, output_dir='./data'):
        """Genera el Markovian Memory Tasks Dataset"""
        print(f"Generando {num_episodes} episodios de MMTD...")

        os.makedirs(output_dir, exist_ok=True)

        data = []
        for i in range(num_episodes):
            # Longitud variable de secuencia
            seq_length = np.random.randint(10, 100)

            # Generar secuencia con dependencias markovianas
            sequence = []
            state = np.random.randn(256).astype(np.float32)

            for t in range(seq_length):
                # Estado markoviano: depende del estado anterior + ruido
                state = 0.8 * state + 0.2 * np.random.randn(256).astype(np.float32)
                sequence.append(state.copy())

            # Target de memoria (últimos 16 estados promediados)
            memory_target = np.mean(sequence[-16:], axis=0)[:16].astype(np.float32)

            data.append({
                'sequence': sequence,
                'sequence_length': seq_length,
                'memory_target': memory_target,
                'episode_id': f'episode_{i:06d}'
            })

        # Guardar en formato Parquet
        df = pd.DataFrame(data)
        df.to_parquet(os.path.join(output_dir, 'mmtd_synthetic.parquet'))

        print(f"✅ MMTD generado: {num_episodes} episodios")
        return os.path.join(output_dir, 'mmtd_synthetic.parquet')

    def generate_continuous_thought_streams(self, num_streams=1000, output_dir='./data'):
        """Genera el Continuous Thought Streams Dataset"""
        print(f"Generando {num_streams} streams de CTSD...")

        os.makedirs(output_dir, exist_ok=True)

        with h5py.File(os.path.join(output_dir, 'ctsd_synthetic.h5'), 'w') as f:
            for i in range(num_streams):
                # Longitud variable del stream
                ticks_count = np.random.randint(20, 100)

                # Generar stream de pensamiento continuo
                thought_stream = np.zeros((ticks_count, 256), dtype=np.float32)

                # Estado inicial
                state = np.random.randn(256).astype(np.float32)

                for t in range(ticks_count):
                    # Evolución continua del pensamiento
                    state = 0.9 * state + 0.1 * np.random.randn(256).astype(np.float32)
                    thought_stream[t] = state

                # Calcular score de continuidad
                continuity_score = 1.0 - np.mean(np.diff(thought_stream, axis=0)**2)
                continuity_score = max(0.0, min(1.0, continuity_score))

                # Guardar stream
                stream_group = f.create_group(f'stream_{i:06d}')
                stream_group.create_dataset('thought_stream', data=thought_stream)
                stream_group.attrs['continuity_score'] = continuity_score
                stream_group.attrs['ticks_count'] = ticks_count
                stream_group.attrs['stream_id'] = f'stream_{i:06d}'

        print(f"✅ CTSD generado: {num_streams} streams")
        return os.path.join(output_dir, 'ctsd_synthetic.h5')

    def generate_entropy_certainty_dataset(self, num_samples=1000, output_dir='./data'):
        """Genera el Entropy-Certainty Calibration Dataset"""
        print(f"Generando {num_samples} muestras de ECCD...")

        os.makedirs(output_dir, exist_ok=True)

        # Generar activaciones neuronales
        activations = np.random.randn(num_samples, 512).astype(np.float32)

        # Calcular certezas objetivo usando softmax y entropía
        target_certainties = []
        entropy_normalized = []

        for i in range(num_samples):
            # Aplicar softmax
            probs = np.exp(activations[i]) / np.sum(np.exp(activations[i]))

            # Calcular entropía
            entropy = -np.sum(probs * np.log(probs + 1e-8))
            max_entropy = np.log(512)  # Entropía máxima
            norm_entropy = entropy / max_entropy

            # Certeza = 1 - entropía normalizada
            certainty = 1.0 - norm_entropy

            target_certainties.append(certainty)
            entropy_normalized.append(norm_entropy)

        target_certainties = np.array(target_certainties, dtype=np.float32)
        entropy_normalized = np.array(entropy_normalized, dtype=np.float32)
        sample_ids = np.arange(num_samples, dtype=np.int64)

        # Guardar en formato NPZ
        np.savez_compressed(
            os.path.join(output_dir, 'eccd_synthetic.npz'),
            activations=activations,
            target_certainty=target_certainties,
            entropy_normalized=entropy_normalized,
            sample_id=sample_ids
        )

        print(f"✅ ECCD generado: {num_samples} muestras")
        return os.path.join(output_dir, 'eccd_synthetic.npz')

    def generate_all_datasets(self, output_dir='./data', small_scale=True):
        """Genera todos los datasets para CTM v5.0"""
        print("🚀 Generando todos los datasets CTM v5.0...")

        if small_scale:
            # Versiones pequeñas para pruebas
            sizes = {
                'dvsd': 1000,
                'mmtd': 500,
                'ctsd': 500,
                'eccd': 1000
            }
        else:
            # Versiones completas
            sizes = {
                'dvsd': 100000,  # 100K muestras
                'mmtd': 50000,   # 50K episodios
                'ctsd': 50000,   # 50K streams
                'eccd': 100000   # 100K muestras
            }

        generated_files = {}

        # Generar cada dataset
        generated_files['dvsd'] = self.generate_dual_vector_sequences(
            sizes['dvsd'], output_dir
        )
        generated_files['mmtd'] = self.generate_markovian_memory_tasks(
            sizes['mmtd'], output_dir
        )
        generated_files['ctsd'] = self.generate_continuous_thought_streams(
            sizes['ctsd'], output_dir
        )
        generated_files['eccd'] = self.generate_entropy_certainty_dataset(
            sizes['eccd'], output_dir
        )

        print("✅ Todos los datasets generados exitosamente!")
        return generated_files


if __name__ == "__main__":
    # Ejemplo de uso
    generator = CTMv5DatasetGenerator()

    # Generar datasets de prueba (pequeños)
    files = generator.generate_all_datasets(output_dir='./data', small_scale=True)

    print("\n📁 Archivos generados:")
    for dataset, filepath in files.items():
        print(f"   {dataset}: {filepath}")
