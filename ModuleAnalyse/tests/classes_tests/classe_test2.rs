use ndarray::Array2;

use crate::{
    feed_forward::FeedForward, layer_norm::LayerNorm, llm::Layer, self_attention::SelfAttention,
};

pub struct TransformerBlock {
    attention: SelfAttention,
    feed_forward: FeedForward,
    norm1: LayerNorm, // After attention
    norm2: LayerNorm, // After feed forward
}

impl TransformerBlock {
    pub fn new(embedding_dim: usize, hidden_dim: usize) -> Self {
        TransformerBlock {
            attention: SelfAttention::new(embedding_dim),
            feed_forward: FeedForward::new(embedding_dim, hidden_dim),
            norm1: LayerNorm::new(embedding_dim),
            norm2: LayerNorm::new(embedding_dim),
        }
    }
}