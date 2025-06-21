#include <vector>
#include <iostream>
#include <cmath>

class CachedSelfAttention {
public:
    CachedSelfAttention(int dim, int heads)
        : dim_(dim), heads_(heads), head_dim_(dim / heads) {}

    void reset_cache() {
        cache_k_.clear();
        cache_v_.clear();
    }

    std::vector<float> forward(const std::vector<float>& x, bool use_cache) {
        int seq_len = x.size() / dim_;
        std::vector<float> q = x;
        std::vector<float> k = x;
        std::vector<float> v = x;

        if (use_cache && !cache_k_.empty()) {
            k.insert(k.begin(), cache_k_.begin(), cache_k_.end());
            v.insert(v.begin(), cache_v_.begin(), cache_v_.end());
        }

        if (use_cache) {
            cache_k_ = k;
            cache_v_ = v;
        }

        int total_len = k.size() / dim_;
        std::vector<float> out(seq_len * dim_, 0.0f);

        for (int h = 0; h < heads_; ++h) {
            int offset = h * head_dim_;
            for (int i = 0; i < seq_len; ++i) {
                for (int j = 0; j < total_len; ++j) {
                    float score = 0.0f;
                    for (int d = 0; d < head_dim_; ++d) {
                        score += q[i * dim_ + offset + d] * k[j * dim_ + offset + d];
                    }
                    score /= std::sqrt(static_cast<float>(head_dim_));
                    for (int d = 0; d < head_dim_; ++d) {
                        out[i * dim_ + offset + d] += score * v[j * dim_ + offset + d];
                    }
                }
            }
        }

        return out;
    }

private:
    int dim_;
    int heads_;
    int head_dim_;
    std::vector<float> cache_k_;
    std::vector<float> cache_v_;
};

int main() {
    CachedSelfAttention attn(8, 2);
    std::vector<float> step1(8, 1.0f);
    auto out1 = attn.forward(step1, true);

    std::vector<float> step2(8, 2.0f);
    auto out2 = attn.forward(step2, true);

    std::cout << "cached sequence length: " << out2.size() / 8 << std::endl;
    attn.reset_cache();
    return 0;
}
